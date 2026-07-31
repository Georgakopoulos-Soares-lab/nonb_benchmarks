import torch
from torch import nn
import transformers
from transformers import BertTokenizer, BertForTokenClassification
import numpy as np
from Bio import SeqIO
from io import StringIO, BytesIO
from tqdm import tqdm
import pickle
import scipy
from scipy import ndimage
import argparse

def seq2kmer(seq, k):
    kmer = [seq[x:x+k] for x in range(len(seq)+1-k)]
    return kmer

def split_seq(seq, length = 512, pad = 16):
    res = []
    for st in range(0, len(seq), length - pad):
        end = min(st+512, len(seq))
        res.append(seq[st:end])
    return res

def stitch_np_seq(np_seqs, pad = 16):
    res = np.array([])
    for seq in np_seqs:
        res = res[:-pad]
        res = np.concatenate([res,seq])
    return res

parser = argparse.ArgumentParser("Z-DNABERT benchmark run.")
parser.add_argument("model_dir", help="A directory containing the required files for the machine learning model")
parser.add_argument("input_fasta", help="The FASTA file used for the benchmark")
parser.add_argument("output_txt", help="The TXT file containing the results")
args = parser.parse_args()

model_confidence_threshold = 0.5
minimum_sequence_length = 10

tokenizer = BertTokenizer.from_pretrained(args.model_dir)
model = BertForTokenClassification.from_pretrained(args.model_dir)
model.cuda()
model.eval()

out = []

print(args.input_fasta)
out.append(args.input_fasta)
result_dict = {}
for seq_record in SeqIO.parse(args.input_fasta, 'fasta'):
    kmer_seq = seq2kmer(str(seq_record.seq).upper(), 6)
    seq_pieces = split_seq(kmer_seq)
    print(seq_record.name)
    out.append(seq_record.name)
    with torch.no_grad():
        preds = []
        for seq_piece in tqdm(seq_pieces):
            input_ids = torch.LongTensor(tokenizer.encode(' '.join(seq_piece), add_special_tokens=False))
            outputs = torch.softmax(model(input_ids.cuda().unsqueeze(0))[-1],axis = -1)[0,:,1]
            preds.append(outputs.cpu().numpy())
    result_dict[seq_record.name] = stitch_np_seq(preds)

    labeled, max_label = scipy.ndimage.label(result_dict[seq_record.name]>model_confidence_threshold)
    print('  start     end')
    out.append('  start     end')
    for label in range(1, max_label+1):
        candidate = np.where(labeled == label)[0]
        candidate_length = candidate.shape[0]
        if candidate_length>minimum_sequence_length:
            print('{:8}'.format(candidate[0]), '{:8}'.format(candidate[-1]))
            out.append('{:8}'.format(candidate[0]) + '{:8}'.format(candidate[-1]))

print()

with open(args.output_txt, "w") as fh:
    for item in out:
        fh.write("%s\n" % item)