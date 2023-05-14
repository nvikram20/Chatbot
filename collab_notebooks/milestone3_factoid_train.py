# -*- coding: utf-8 -*-
"""milestone3_factoid_train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18VtRaEuBKJm5VxoTSpMTXINRhbAepNRW
"""

# Commented out IPython magic to ensure Python compatibility.
# %env CUDA_LAUNCH_BLOCKING=1

import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

! pip install transformers==4.27.4

! pip install torchtext==0.10.1

import torch

device = torch.device("cuda")
torch.cuda.init()

torch.cuda.empty_cache()

from google.colab import drive
drive.mount('/content/gdrive')

from transformers import GPT2Tokenizer, GPT2Config, GPT2LMHeadModel, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

config = GPT2Config(vocab_size=50257, n_positions=512, n_ctx=512, n_embd=512, n_layer=12, n_head=8)

# model = GPT2LMHeadModel(config)
model = GPT2LMHeadModel.from_pretrained('gpt2')

train_data = TextDataset(tokenizer=tokenizer, file_path="/content/gdrive/My Drive/dataset/combined_factoid_train.txt", block_size=256)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir='/content/gdrive/My Drive/models/',
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=8,
    save_steps=1000,
    save_total_limit=2,
    prediction_loss_only=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    data_collator=data_collator,
)

len(train_data.examples)

trainer.train()

trainer.save_model("/content/gdrive/My Drive/model/factoid_generator.pt")

torch.save(model.state_dict(), "/content/gdrive/My Drive/model/factoid_generator_2.pt")

# def getResponse(input_text, model,tokenizer, device):
#   input_ids = tokenizer.encode(input_text, return_tensors='pt')
#   input_ids = input_ids.to(device)
#   attention_mask = torch.LongTensor([1] * len(input_ids))
#   output_ids = model.generate(input_ids,pad_token_id=tokenizer.eos_token_id, max_length=50, num_beams=5, 
#                                       num_return_sequences=3, 
#                                       no_repeat_ngram_size=2, 
#                                       early_stopping=True)
#   output_text1 = tokenizer.decode(output_ids[0], skip_special_tokens=True)
#   output_text2 = tokenizer.decode(output_ids[1], skip_special_tokens=True)
#   output_text3 = tokenizer.decode(output_ids[2], skip_special_tokens=True)
#   # parts = output_text.split("\n")
#   # bot_response = parts[-2][4:] 
#   # bot_response.strip()
#   return output_text1, output_text2, output_text3

import re
def getResponse(input_text, model,tokenizer, device):
  input_ids = tokenizer.encode(input_text, return_tensors='pt')
  if(len(input_ids)<=0):
    print(input_text)
    return None
  input_ids = input_ids.to(device)
  model = model.to(device)
  output_ids = model.generate(input_ids,pad_token_id=tokenizer.eos_token_id, max_length=70,early_stopping=True)
  output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
  messages = output_text.split("\n")
  first_bot_response = None
  for message in messages:
    if message.startswith("Bot:"):
        first_bot_response = message.strip()
        break
  return first_bot_response

input_text = "User: Who is the president of the United States?"

input_text = "User: Which countries are in North America?"
bot_response = getResponse(input_text, model, tokenizer, device)
print(bot_response)
