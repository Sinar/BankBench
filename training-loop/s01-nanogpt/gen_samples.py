#!/usr/bin/env python3
"""Generate samples from checkpoints at different steps (S-01 deliverable).

Usage:
  python gen_samples.py <ckpt.pt> <tag>
Writes samples to out/samples_<tag>.txt

Char-level: seed prompt is a few chars, samples are 200 chars each.
"""
import sys
import pickle
import torch
import numpy as np
from model import GPTConfig, GPT

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    ckpt_path, tag = sys.argv[1], sys.argv[2]

    meta = pickle.load(open("data/shakespeare_char/meta.pkl", "rb"))
    stoi, itos = meta["stoi"], meta["itos"]

    checkpoint = torch.load(ckpt_path, map_location="mps")
    model_args = checkpoint["model_args"]
    for k in ["n_layer", "n_head", "n_embd", "block_size", "bias", "vocab_size"]:
        model_args[k] = checkpoint["model_args"][k]
    gptconf = GPTConfig(**model_args)
    model = GPT(gptconf)
    model.load_state_dict(checkpoint["model"])
    model.to("mps")
    model.eval()

    seeds = [
        "Customer: ",
        "I need to transfer RM",
        "Salam, boleh",
        "Agent: ",
        "Please check my",
    ]

    lines = []
    for seed in seeds:
        x = torch.tensor([[stoi[c] for c in seed]], dtype=torch.long, device="mps")
        with torch.no_grad():
            for _ in range(200):
                logits, _ = model(x)
                logits = logits[:, -1, :] / 0.8
                probs = torch.softmax(logits, dim=-1)
                idx = torch.multinomial(probs, num_samples=1)
                x = torch.cat((x, idx), dim=1)
        text = "".join([itos[i.item()] for i in x[0]])
        lines.append(f"--- seed: {seed!r}\n{text}\n")

    out = f"out/samples_{tag}.txt"
    with open(out, "w") as f:
        f.write(f"# samples from {ckpt_path} (iter {checkpoint['iter_num']})\n")
        f.write("\n".join(lines))
    print(f"wrote {out}")

if __name__ == "__main__":
    main()
