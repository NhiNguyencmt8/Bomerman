import torch
import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):

    # This takes in [1 or BATCH_SIZE, 48, 114] and outputs [1, 19]
    # def __init__(self, w, h, num_classes=19):
    #     super(DQN, self).__init__()
    #     self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
    #     self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
    #     self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
    #     self.fc1 = nn.Linear(64 * 28 * 12, 512)
    #     self.fc2 = nn.Linear(512, num_classes)
    #
    # def forward(self, x):
    #     print(x.shape, "In DQN")
    #     x = self.pool(F.relu(self.conv1(x.unsqueeze(1))))
    #     x = self.pool(F.relu(self.conv2(x)))
    #     x = x.view(-1, 64 * 28 * 12)
    #     x = F.relu(self.fc1(x))
    #     x = self.fc2(x)
    #     return x

    # This takes in [1 or BATCH_SIZE, 18, 7] and outputs [1, 19]
    # def __init__(self, w, h, num_classes=9):
    #     super(DQN, self).__init__()
    #     self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
    #     self.conv2 = nn.Conv2d(32, 128, kernel_size=3, stride=1, padding=1)
    #     self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
    #     self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
    #     self.fc1 = nn.Linear(128 * (w//4) * (h//4), 512)
    #     self.fc2 = nn.Linear(512, num_classes)
    #
    # def forward(self, x):
    #     x = x.unsqueeze(1)
    #     x = self.pool1(F.relu(self.conv1(x)))
    #     x = self.pool2(F.relu(self.conv2(x)))
    #     x = x.view(x.size(0), -1)
    #     x = F.relu(self.fc1(x))
    #     x = self.fc2(x)
    #     return x

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 256)
        self.layer2 = nn.Linear(256, 128)
        self.layer3 = nn.Linear(128, 128)
        self.layer4 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        # print(x.shape, "In DQN")
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        return self.layer4(x)