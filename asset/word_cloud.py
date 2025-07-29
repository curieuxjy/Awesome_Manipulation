import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Stopwords to exclude common words from the word cloud
stopwords = set([
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", 
    "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", 
    "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's",
    "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", 
    "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "via", "was", "we", "we'd", "we'll", "we're",
    "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
    "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves", "using", 
])

# 1. Get the paper list from the user
# papers_input = input("Please provide the list of papers:\n")
papers_input = """

- [A Model-Free Approach to Fingertip Slip and Disturbance Detection for Grasp Stability Inference](https://ieeexplore.ieee.org/document/10364337/)
- [AnyTeleop: A General Vision-Based Dexterous Robot Arm-Hand Teleoperation System](https://arxiv.org/abs/2307.04577) [➕](https://yzqin.github.io/anyteleop/)
- [Contact Edit: Artist Tools for Intuitive Modeling of Hand-Object Interactions](https://arxiv.org/abs/2305.02051)
- [Deep Reinforcement Learning of Dexterous Pre-grasp Manipulation for Human-like Functional Categorical Grasping](https://arxiv.org/abs/2307.16752)
- [DexDeform: Dexterous Deformable Object Manipulation with Human Demonstrations and Differentiable Physics](https://arxiv.org/abs/2304.03223) [➕](https://sites.google.com/view/dexdeform)
- [DexPBT: Scaling up Dexterous Manipulation for Hand-Arm Systems with Population Based Training](https://arxiv.org/abs/2305.12127)
- [General In-Hand Object Rotation with Vision and Touch](https://arxiv.org/abs/2309.09979)
- [Getting the Ball Rolling: Learning a Dexterous Policy for a Biomimetic Tendon-Driven Hand with Rolling Contact Joints](https://arxiv.org/abs/2308.02453) [➕](http://tactilesim.csail.mit.edu/)
- [Global Planning for Contact-Rich Manipulation via Local Smoothing of Quasi-dynamic Contact Models](https://arxiv.org/pdf/2206.10787)
- [IndustReal: Transferring Contact-Rich Assembly Tasks from Simulation to Reality](https://arxiv.org/abs/2305.17110) [➕](https://sites.google.com/nvidia.com/industreal)
- [Neural feels with neural fields: Visuo-tactile perception for in-hand manipulation](https://arxiv.org/abs/2312.13469)
- [Perceiving Extrinsic Contacts from Touch Improves Learning Insertion Policies](https://arxiv.org/abs/2309.16652)
- [Rotating without Seeing: Towards In-hand Dexterity through Touch](https://arxiv.org/abs/2303.10880) [➕](https://touchdexterity.github.io/)
- [Sampling-based Exploration for Reinforcement Learning of Dexterous Manipulation](https://arxiv.org/abs/2303.03486)
- [Sequential Dexterity: Chaining Dexterous Policies for Long-Horizon Manipulation](https://arxiv.org/abs/2309.00987)
- [Tacchi: A Pluggable and Low Computational Cost Elastomer Deformation Simulator for Optical Tactile Sensors](https://arxiv.org/abs/2301.08343)
- [UniDexGrasp++: Improving Dexterous Grasping Policy Learning via Geometry-aware Curriculum and Iterative Generalist-Specialist Learning](https://arxiv.org/abs/2304.00464) [➕](https://pku-epic.github.io/UniDexGrasp++/)
- [Visual Dexterity: In-Hand Reorientation of Novel and Complex Object Shapes](https://arxiv.org/abs/2211.11744)

"""

# 2. Ask the user for the title of the picture
# picture_title = input("Please provide the title for the picture (without the .png extension): ")
picture_title = "2023"

# 3. Extract the words from the titles (excluding the links)
titles = re.findall(r"\[(.*?)\]\(.*?\)", papers_input)

keywords = []
for title in titles:
    for word in title.split():
        cleaned_word = re.sub(r'[^a-zA-Z]', '', word).lower()  # Removing non-alphabetic characters and converting to lowercase
        if cleaned_word not in stopwords:
            keywords.append(cleaned_word)

# Counting keyword frequencies
keyword_freq = Counter(keywords)

# 4. Create the word cloud with landscape ratio and save it
wordcloud = WordCloud(width=2000,
                      height=500,
                      colormap="Greens",
                      background_color="rgba(255, 255, 255, 0)",
                      mode="RGBA").generate_from_frequencies(keyword_freq)
plt.figure(figsize=(20,5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()

# Save the image in the same location as the code
file_name = f"{picture_title}.png"
plt.savefig(file_name, bbox_inches="tight", pad_inches=0, transparent=True)
print(f"Word cloud saved as {file_name}")