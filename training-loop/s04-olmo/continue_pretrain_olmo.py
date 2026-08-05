#!/usr/bin/env python3
"""Small continued-pretrain / SFT step on an OLMo-2 checkpoint, same data as S-02.

TODO: confirm the smallest current OLMo-2 checkpoint name on HuggingFace
(e.g. allenai/OLMo-2-... -- check model card for the smallest variant available)
before renting GPU time for this -- 7B is likely too heavy for the $10 budget
stacked on top of S-02's spend.

Run:
  python continue_pretrain_olmo.py --data ../data/sft_train.jsonl
"""
import argparse
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="allenai/OLMo-2-1B")  # TODO: confirm smallest available variant
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, default=Path("out"))
    ap.add_argument("--epochs", type=int, default=1)
    args = ap.parse_args()

    from datasets import load_dataset
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import SFTConfig, SFTTrainer

    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(args.model, trust_remote_code=True)

    dataset = load_dataset("json", data_files=str(args.data))["train"]
    dataset = dataset.map(lambda ex: {"text": f"### Prompt:\n{ex['prompt']}\n\n### Response:\n{ex['completion']}"})

    sft_config = SFTConfig(
        output_dir=str(args.out_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=2,  # smaller than S-02 -- OLMo checkpoints run heavier
        learning_rate=1e-5,
        logging_steps=1,
        save_strategy="epoch",
        report_to=[],
    )
    trainer = SFTTrainer(model=model, args=sft_config, train_dataset=dataset, dataset_text_field="text")
    trainer.train()
    trainer.save_model(str(args.out_dir / "checkpoint-final"))
    print(f"Saved to {args.out_dir / 'checkpoint-final'}")


if __name__ == "__main__":
    main()
