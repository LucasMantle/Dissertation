# This function simply applies the finbert model and returns the sentiment prediction and their scores
def finbert_sentiment(x, pt_model, tokenizer):
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch.nn.functional as F
    import numpy as np
    import pandas as pd

    inputs = tokenizer(x)

    pt_batch = tokenizer(
        [x],
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )

    pt_outputs = pt_model(**pt_batch)
    pt_predictions = F.softmax(pt_outputs.logits, dim=-1)

    pred_pos = np.argmax(pt_predictions.detach().numpy()[0])
    return pd.Series([pt_predictions.detach().numpy()[0][0],
                      pt_predictions.detach().numpy()[0][1],
                      pt_predictions.detach().numpy()[0][2],
                      ['Pos', 'Neg', 'Neu'][pred_pos]])
