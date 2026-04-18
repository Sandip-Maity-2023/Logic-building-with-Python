import torch.nn as nn
from torchvision import models


class HybridModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        weights = models.MobileNet_V3_Small_Weights.DEFAULT
        backbone = models.mobilenet_v3_small(weights=weights)
        self.backbone = backbone.features
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.projection = nn.Linear(576, 576)

        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=576,
                nhead=8,
                batch_first=True,
            ),
            num_layers=4,
        )

        self.fc = nn.Linear(576, num_classes)

    def forward(self, x):
        feat = self.backbone(x)
        feat = feat.flatten(2).transpose(1, 2)
        feat = self.projection(feat)
        out = self.transformer(feat)
        out = out.mean(dim=1)
        return self.fc(out)
