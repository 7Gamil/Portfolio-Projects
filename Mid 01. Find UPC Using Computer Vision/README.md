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
```bach
pip install -r requirments.txt
```

## How to use
```bach
python Main.py
```

## Demo video
https://github.com/user-attachments/assets/4111857a-446b-4635-91e2-326eef1cb603


  
