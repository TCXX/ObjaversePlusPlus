import torch
import torch.nn as nn
from torchvision import models, transforms
import torch.nn.functional as F

class AttentionLayer(nn.Module):
    def __init__(self, feature_dim):
        super(AttentionLayer, self).__init__()
        self.fc = nn.Linear(feature_dim, 1)

    def forward(self, x):
        # x shape: (batch_size, num_views, feature_dim)
        attention_weights = torch.sigmoid(self.fc(x))  # Shape: (batch_size, num_views, 1)
        attention_weights = F.softmax(attention_weights, dim=1)  # Normalize over views
        weighted_features = x * attention_weights  # Apply weights to features
        aggregated_features = torch.sum(weighted_features, dim=1)  # Sum over views
        return aggregated_features

class MultiView3DModelClassifierWithAttention(nn.Module):
    def __init__(self, num_layers=1):
        super(MultiView3DModelClassifierWithAttention, self).__init__()
        # Use ResNet50 pretrained on ImageNet for feature extraction
        resnet = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        self.feature_extractor = nn.Sequential(*list(resnet.children())[:-1])
        # Disable training for the feature extractor
        for param in self.feature_extractor.parameters():
            param.requires_grad = False

        # RNN (LSTM) for processing the sequential features
        self.rnn = nn.LSTM(
            input_size=2048, hidden_size=512, num_layers=num_layers, batch_first=True
        )
        self.attention = AttentionLayer(512)  # Assuming output of RNN is 512 features
        # four metadata: vertexCount,faceCount,viewCount,likeCount
        self.meta_fc = nn.Linear(4, 16)  # Process metadata

        # Classification heads
        # Assuming labels are stored as a tuple:
        # (style, score, is_multi_object, is_weird, is_scene, is_figure, is_transparent, density)
        self.style_head = nn.Linear(512 + 16, 7)  # Style (0 to 6)
        self.score_head = nn.Linear(512 + 16, 4)  # Score (0 to 3)
        self.multi_object_head = nn.Linear(512 + 16, 1)  # Is_multi_object (bool)
        self.weird_head = nn.Linear(512 + 16, 1)  # Is_weird (bool)
        self.scene_head = nn.Linear(512 + 16, 1)  # Is_scene (bool)
        self.figure_head = nn.Linear(512 + 16, 1)  # Is_figure (bool)
        self.transparent_head = nn.Linear(512 + 16, 1)  # Is_transparent (bool)
        self.single_color_head = nn.Linear(512 + 16, 1)  # Is_single_color (bool)
        self.density_head = nn.Linear(512 + 16, 3)  # Density (0 to 2)

    def forward(self, x, metadata):
        # x is expected to be of shape (batch_size, num_views, C, H, W)
        batch_size, num_views, C, H, W = x.size()
        x = x.view(batch_size * num_views, C, H, W).float()
        metadata = metadata.float()
        features = self.feature_extractor(x)
        features = features.view(batch_size, num_views, -1)
        meta_out = nn.functional.relu(self.meta_fc(metadata))  # Process metadata

        # RNN
        rnn_out, (hn, _) = self.rnn(features)
        # Apply attention to the outputs of the RNN
        
        attention_out = self.attention(rnn_out)
        #print(attention_out.shape)
        #print(meta_out.shape)
        # Combine features with metadata
        combined = torch.cat((attention_out, meta_out), dim=1)

        # Predictions
        style = self.style_head(combined)
        score = self.score_head(combined)
        is_multi_object = self.multi_object_head(combined)
        is_weird = self.weird_head(combined)
        is_scene = self.scene_head(combined)
        is_figure = self.figure_head(combined)
        is_transparent = self.transparent_head(combined)
        is_single_color = self.single_color_head(combined)
        density = self.density_head(combined)

        return (
            style,
            score,
            is_multi_object,
            is_weird,
            is_scene,
            is_figure,
            is_transparent,
            is_single_color,
            density,
        )

# Instantiate the model
model = MultiView3DModelClassifierWithAttention()

# Example tensor for 40 views (assuming batch size of 1 and 3x224x224 images)
# x = torch.randn(1, 40, 3, 224, 224)
# style, score, is_multi_object, is_transparent, is_figure = model(x)
