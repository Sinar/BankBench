#!/usr/bin/env python3
"""LoRA fine-tune a small base model on BankBench-MY-shaped SFT data.

This is the stage that answers securefast.ai's "have you run the training
loop" question with a real, measurable behavior-change claim. Keep the model
small (0.5B-2B) so this runs on a single rented GPU in under an hour.

Run (local dry run, no GPU needed, just checks the loop doesn't crash):
  python finetune_lora.py --model Qwen/Qwen2.5-0.5B-Instruct --dry-run --max-steps 5

Run (real, on a rented GPU):
  python finetune_lora.py --model Qwen/Qwen2.5-0.5B-Instruct --epochs 3
"""
import argparse
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--lora-r", type=int, default=8)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--out-dir", type=Path, default=Path("out"))
    ap.add_argument("--dry-run", action="store_true", help="tiny run to sanity-check the loop, no real training")
    ap.add_argument("--max-steps", type=int, default=None)
    args = ap.parse_args()

    from datasets import load_dataset
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import SFTConfig, SFTTrainer

    train_path = DATA_DIR / "sft_train.jsonl"
    if not train_path.exists():
        raise SystemExit(f"{train_path} missing -- run data/prepare_bankbench_sft.py first")

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model)

    lora_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_r * 2,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    dataset = load_dataset("json", data_files=str(train_path))["train"]

    def format_example(ex):
        return {"text": f"### Prompt:\n{ex['prompt']}\n\n### Response:\n{ex['completion']}"}

    dataset = dataset.map(format_example)

    sft_config = SFTConfig(
        output_dir=str(args.out_dir),
        num_train_epochs=1 if args.dry_run else args.epochs,
        per_device_train_batch_size=args.batch_size,
        learning_rate=args.lr,
        max_steps=args.max_steps if args.dry_run else -1,
        logging_steps=1,
        save_strategy="epoch",
        report_to=[],
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_config,
        train_dataset=dataset,
        dataset_text_field="text",
    )
    trainer.train()

    final_dir = args.out_dir / "checkpoint-final"
    trainer.save_model(str(final_dir))
    tokenizer.save_pretrained(str(final_dir))
    print(f"Saved fine-tuned checkpoint to {final_dir}")


if __name__ == "__main__":
    main()
