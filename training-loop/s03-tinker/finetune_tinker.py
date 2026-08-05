#!/usr/bin/env python3
"""Reproduce S-02's fine-tune using Tinker's low-level training API.

TODO: this is a structural skeleton against Tinker's documented primitives
(forward_backward, optim_step, sampling) as of when this file was written --
confirm current SDK method names/signatures against Tinker's own docs before
running, the API surface may have moved.

Run:
  python finetune_tinker.py --data ../data/sft_train.jsonl
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--base-model", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--out", type=Path, default=Path("tinker_run_log.json"))
    args = ap.parse_args()

    # import tinker  # TODO: confirm package name / install path from current Tinker docs
    #
    # client = tinker.ServiceClient()
    # training_client = client.create_lora_training_client(base_model=args.base_model)
    #
    # examples = [json.loads(l) for l in args.data.read_text().splitlines() if l.strip()]
    # for step, batch in enumerate(batched(examples, batch_size=4)):
    #     datums = [tinker.Datum(prompt=ex["prompt"], target=ex["completion"]) for ex in batch]
    #     fwd_bwd = training_client.forward_backward(datums, loss_fn="cross_entropy")
    #     optim_step = training_client.optim_step(adam_params)
    #     log.append({"step": step, "loss": fwd_bwd.result().loss})
    #
    # sampling_client = training_client.save_weights_and_get_sampling_client(name="bankbench-my-ft")

    raise NotImplementedError(
        "Fill in the Tinker SDK calls above once API access is confirmed -- "
        "this skeleton exists so the loop *shape* (forward_backward -> optim_step -> "
        "sample) is planned before you're paying for Tinker compute time."
    )


if __name__ == "__main__":
    main()
