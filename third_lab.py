import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
model = AutoModelForMaskedLM.from_pretrained("DeepPavlov/rubert-base-cased")
model.eval()

text = 'Уже тогда старик почувствовал, что он променял кукушку на ястреба. Правда, что по закону, как разумел его старик, надо было бездетному идти за семейного. У Акима было четверо детей, у Петра никого, но работник Петр был такой же, как и отец: ловкий, сметливый, сильный, выносливый и, главное, трудолюбивый. Он [MASK] работал.'

inputs = tokenizer(text, return_tensors="pt")

mask_token_index = (inputs["input_ids"] == tokenizer.mask_token_id).nonzero(as_tuple=True)[1]

with torch.no_grad():
    outputs = model(input_ids=inputs["input_ids"],token_type_ids=inputs["token_type_ids"],attention_mask=inputs["attention_mask"])
    logits = outputs.logits

mask_logits = logits[0, mask_token_index[0], :]
top_5_tokens = torch.topk(mask_logits, 5, dim=0).indices.tolist()

print("текст:", text)
print("\nCлова:")

for i, token_id in enumerate(top_5_tokens, start=1):
    print(tokenizer.decode([token_id]))