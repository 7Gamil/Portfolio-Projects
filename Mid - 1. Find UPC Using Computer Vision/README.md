# Find UPC Using computer Vision `15/11/2024`
## Brief
Find UPC Using Computer Vision to make your life easier by automating the manual work for you.

## Steps
1. **Collect** the product names and images we want to check thier UPC.
2. **put** product names and path / URL of images in CSV file.
2.1 **the structure of CSV file:**
    ```
    Name, Image URL / Path, UPC, Accuracy
    Lay's Sour Cream & Onion Potato Chips, imgs/1.jpeg,,
    Lay's Lightly Salted Potato Chips, imgs/2.jpeg,,
    ```
3. **Edit** the target website URL in `Main.py`.
4. **Use** `Mouse Position Finder.py` to find coordinates on the screen.
    4.1 **Edit** the image product coordinates for the target website in `Main.py`.
    4.2 **Edit** the coordinates of your UPC number in `my_package/utils.py`.
5. **Add** the chrome extension [Buster: Captcha Solver for Humans](https://chromewebstore.google.com/detail/buster-captcha-solver-for/mpbjkejclgfgadiemmefgebjfooflfhl) to your chrome-based browser

## Prerequisites
Install Required libraries
`pip install -r requirments.txt`

## How to use
`python Main.py`

## Demo video Example to show case
[Video Example](https://raw.githubusercontent.com/7Gamil/MyProjects/refs/heads/main/Mid%20-%201.%20Find%20UPC%20Using%20Computer%20Vision/Resources/Demo1.mp4)

## Demo Video Example to Showcase
<video width="640" height="360" controls>
  <source src="Resources/Demo1.mp4" type="video/mp4">
</video>

<figure class="video_container">
 <video controls="true" allowfullscreen="true">
 <source src="./Resources/Demo1.mp4" type="video/mp4">
 </video>
</figure>

[![Watch the video](https://opencode.md/wp-content/uploads/2023/08/Top-8-facts-about-Linux-2.jpg)](https://raw.githubusercontent.com/7Gamil/MyProjects/refs/heads/main/Mid%20-%201.%20Find%20UPC%20Using%20Computer%20Vision/Resources/Demo1.mp4?token=GHSAT0AAAAAACVXPPY5UYEBCCYTE2KST5T6Z2ZTHOA)

<video src="Resources/Demo1.mp4" controls title="Title"></video>  

<video src="resource/demo1.mp4" controls title="Demo Video"></video>  
