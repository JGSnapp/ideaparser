from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from sqlalchemy.orm import Session
from .models import IdeaCard, DailyHotTopic
from .config import OPENAI_API_KEY

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is required for idea generation")


def generate_idea_cards(db: Session):
    top_topics = db.query(DailyHotTopic).order_by(DailyHotTopic.trend_score.desc()).limit(10).all()
    if not top_topics:
        return
    llm = OpenAI(temperature=0)
    search = DuckDuckGoSearchRun()
    tools = [Tool(name='web_search', func=search.run, description='search the web')]
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description")

    template = (
        "Generate idea card for '{topic}' in format:\n"
        "Problem: ...\nSolution: ...\nTAM: ...\nWhy Now: ...\nNext Steps: ..."
    )
    prompt = PromptTemplate(input_variables=['topic'], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)

    for t in top_topics:
        result = chain.run(topic=t.keyword)
        parts = {p.split(':')[0].strip().lower(): p.split(':')[1].strip() for p in result.split('\n') if ':' in p}
        card = IdeaCard(
            keyword=t.keyword,
            problem=parts.get('problem', ''),
            solution=parts.get('solution', ''),
            tam=parts.get('tam', ''),
            why_now=parts.get('why now', ''),
            next_steps=parts.get('next steps', ''),
        )
        db.add(card)
    db.commit()


def generate_hypothesis_card(db: Session, description: str) -> IdeaCard:
    llm = OpenAI(temperature=0)
    template = (
        "For the following idea description generate TAM, Competitors and Risks:\n"
        "{desc}\nTAM: \nCompetitors: \nRisks:"
    )
    prompt = PromptTemplate(input_variables=['desc'], template=template)
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(desc=description)
    parts = {p.split(':')[0].strip().lower(): p.split(':')[1].strip() for p in result.split('\n') if ':' in p}
    card = IdeaCard(
        keyword=description[:50],
        problem='',
        solution='',
        tam=parts.get('tam', ''),
        why_now='',
        next_steps='',
        hypothesis=description + '\n' + result
    )
    db.add(card)
    db.commit()
    return card
