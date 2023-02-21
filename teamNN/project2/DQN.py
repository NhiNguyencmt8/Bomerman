import torch
import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):

    def __init__(self, input_width, input_height, n_actions):
        super(DQN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        self.fc4 = nn.Linear(self.get_conv_output(input_width, input_height), 512)
        self.fc5 = nn.Linear(512, n_actions)

    def get_conv_output(self, width, height):
        fake_input = torch.zeros((1, 1, height, width))
        x = self.conv1(fake_input)
        x = self.conv2(x)
        x = self.conv3(x)
        return int(x.view(1, -1).size(1))

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.fc4(x.view(x.size(0), -1)))
        return self.fc5(x)
