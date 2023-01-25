# Spam-Video-Detection-System
Spam Video Detecting System for Self-media Website Bilibili  
We design a span video detector. Given impression information before user watched the video(title/cover image/clicks/type), output the possibility of being a spam video. 

We define spam video as following:  
1. High clicks with low collections or likes.
2. May have attracting cover image containing pornography or bizarre features.
3. May have attracting title not in line with the fact or raising curiosity.

## PHPMySQL-Crawler
Author: https://github.com/GANGE666  
Multiprocess crawler for getting comprehensive information of videos on bilibili. Including avid, title, times of view, cover picture address, etc.  
## BaitOrNot
Author: https://github.com/ZhiyangZhang98  
Output a score indicating whether one video is a bait. It takes number of favorites, coins, views and comments into consideration.  
## BERT-NLP
Use BERT model for natural language processing. It was casted as a binary classifier here.  
Author: https://github.com/XiaoSanGit  
BERT source repo: https://github.com/google-research/bert  
## ResNet-Multimedia
Use Resnet_v2_101 for video cover image spam classification.  
Author: me (adonis-dym) https://github.com/adonis-dym

## Bilibili Chrome Plugin
Author: https://github.com/GANGE666

Use our results to tag videos in browsers.

