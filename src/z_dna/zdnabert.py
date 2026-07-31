import torch
from torch import nn
import transformers
from transformers import BertTokenizer, BertForTokenClassification
import numpy as np
from Bio import SeqIO
from io import StringIO, BytesIO
from google.colab import drive, files
from tqdm import tqdm
import pickle
import scipy
from scipy import ndimage

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

model = 'HG kouzine' #@param ["HG chipseq", "HG kouzine", "MM chipseq", "MM kouzine"]
model_confidence_threshold = 0.5 #@param {type:"number"}
minimum_sequence_length = 10 #@param {type:"integer"}

if model == 'HG chipseq':
    model_id = '1VAsp8I904y_J0PUhAQqpSlCn1IqfG0FB'
elif model == 'HG kouzine':
    model_id = '1dAeAt5Gu2cadwDhbc7OnenUgDLHlUvkx'
elif model == 'MM curax':
    model_id = '1W6GEgHNoitlB-xXJbLJ_jDW4BF35W1Sd'
elif model == 'MM kouzine':
    model_id = '1dXpQFmheClKXIEoqcZ7kgCwx6hzVCv3H'


!gdown $model_id
!gdown 10sF8Ywktd96HqAL0CwvlZZUUGj05CGk5
!gdown 16bT7HDv71aRwyh3gBUbKwign1mtyLD2d
!gdown 1EE9goZ2JRSD8UTx501q71lGCk-CK3kqG
!gdown 1gZZdtAoDnDiLQqjQfGyuwt268Pe5sXW0 
    

!mkdir 6-new-12w-0
!mv pytorch_model.bin 6-new-12w-0/
!mv config.json 6-new-12w-0/
!mv special_tokens_map.json 6-new-12w-0/
!mv tokenizer_config.json 6-new-12w-0/
!mv vocab.txt 6-new-12w-0/

tokenizer = BertTokenizer.from_pretrained('6-new-12w-0/')
model = BertForTokenClassification.from_pretrained('6-new-12w-0/')
model.cuda()

uploaded = files.upload()
for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

out = []
for key in uploaded.keys():
    print(key)
    out.append(key)
    result_dict = {}
    for seq_record in SeqIO.parse(StringIO(BytesIO(uploaded[key]).read().decode('UTF-8')), 'fasta'):
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
    
    with open(key + '.preds.pkl',"wb") as fh:
      pickle.dump(result_dict, fh)
    print()

with open('text_predictions.txt',"w") as fh:
    for item in out:
        fh.write("%s\n" % item)

files.download('text_predictions.txt') 