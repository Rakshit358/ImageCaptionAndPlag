import subprocess
import sys
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# BASE_DIR -> backend/
def _run_script2(script_relative_path, env=None):
    script_path = os.path.join(BASE_DIR, script_relative_path)

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        env=env
    )

    return {
        "status": "success" if result.returncode == 0 else "failed",
        "return_code": result.returncode,
        "output": result.stdout,
        "stderr": result.stderr
    }

def _run_script1(script_relative_path):
    script_path = os.path.join(BASE_DIR, script_relative_path)

    if not os.path.exists(script_path):
        return {
            "status": "error",
            "message": "Script not found",
            "path": script_path
        }

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True
    )

    return {
        "status": "success" if result.returncode == 0 else "failed",
        "return_code": result.returncode,
        "output": result.stdout,
        "stderr": result.stderr
    }


def run_news_db_creation():
    """Runs fetch_news.py"""
    return _run_script1(
        "src/plagiarism/news_plag/fetch_news.py"
    )


def run_test_news_plagiarism(query=None):
    """Runs test_search.py"""
    env = os.environ.copy()

    if query:
        env["SEARCH_QUERY"] = query

    return _run_script2(
        "src/plagiarism/news_plag/test_search.py",
        env=env
    )


def run_blog_db_creation():
    """Runs fetch_test_blogs.py"""
    return _run_script1(
        "src/plagiarism/blog_plag/fetch_test_blogs.py"
    )
def run_test_blog_plagiarism(query=None):
    """Runs test_search.py"""
    env = os.environ.copy()

    if query:
        env["SEARCH_QUERY"] = query

    return _run_script2(
        "src/plagiarism/blog_plag/test_search.py",
        env=env
    )


def run_article_db_creation():
    """Runs fetch_arxiv_papers.py"""
    return _run_script1(
        "src/plagiarism/research_papers/fetch_arxiv_papers.py"
    )

def run_test_article_plagiarism(query=None):
    """Runs test_search.py"""
    env = os.environ.copy()

    if query:
        env["SEARCH_QUERY"] = query

    return _run_script2(
        "src/plagiarism/research_papers/test_search.py",
        env=env
    )