.PHONY: install test train eval chat serve demo clean

install:
	pip install -e ".[all,dev]"

test:
	pytest tests/ -v

train:
	python scripts/download_data.py --all
	python trainer/pretrain.py --dim 512 --n_layers 8
	python trainer/sft.py --load_from ./checkpoints/pretrain_512.pth

eval:
	python eval/advertising_bench.py --quick

chat:
	python -m miniagent.chat

serve:
	python scripts/serve_openai_api.py --port 8080

demo:
	pip install streamlit
	streamlit run scripts/web_demo.py

lint:
	ruff check .

clean:
	rm -rf checkpoints/ dataset/*.jsonl __pycache__ .pytest_cache
	find . -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true

download-data:
	python scripts/download_data.py --all
