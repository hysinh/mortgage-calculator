# Happy Cake Friends Memory Game
  ![screenshot of landing page](docs/documentation/Screenshot_amiresponsive.png)

  [View Live Project Here](https://mortgage-comparison-tool-c884f78efc79.herokuapp.com/)

## Introduction
The Happy Cake Friends Memory Game is a simple, fun online game for all ages.

## CONTENTS  
  
* [User Experience)](#user-experience)
  * [User Stories](#user-stories) 
* [Design](#design)
  * [Site Design](#site-design)
  * [Wireframes](#wireframes)
  * [Colour Scheme](#colour)
  * [Typography](#typography)
* [Features](#features)
  * [Card Grid](#card-grid)
  * [Play Button](#play-button)
  * [Player Tries Remaining](#player-tries-remaining)
  * [Win Game and Lose Game Modals](#win-game-and-lose-game-modals)
  * [Footer](#footer)  
  * [Favicon](#favicon)  
* [Future Features](#future-features)
* [Technologies](#technologies)
  * [Languages Used](#languages-used)
  * [Technologies and Programs Used](#technologies-and-programs-used)
  * [Deployment](#deployment)
* [Testing](#testing)
  * [HTML Validation](#html-validation)
  * [CSS Validationn](#css-validation)
  * [Javascript Validationn](#javascript-validation)
  * [Lighthouse Performance Audits via Chrome Dev Tools](#lighthouse-performace-audit-via-chrome-dev-tools)
  * [Manual Testing](#manual-testing)
  * [Bugs and Fixes](#bugs-and-fixes)
  * [Unfixed Bugs](#unfixed-bugs)
* [Credits](#credits) 

  
---   

## User Experience
The Happy Cake Friends Memory Game is a fun, online, memory matching game for all ages and genders. It is a simple game designed to entertain it's user with a brief, challenging game of memory. The game can be played to entertain oneself at any time! The User Interface features bright and attractive colors and happy illustrated characters on each of the cards.
- ### Visitor Goal
  Happy Cake Friends visitors can range in age and genger but they are all generally looking for a simple, online game to entertain them featuring the Happy Cake Friends characters. The website offers a short reprieve from the cares of daily life and offers entertainment via a mentally challenging memory exercise.
- ### User stories
  1. User looking to play a simple game while waiting for public transport.
  2. User looking for a simple memory game to play while waiting (e.g. waiting at the GP office or riding the bus).
  3. User is a child with a parent who needs them to be occupied with a simple, safe and entertaining memory game that can be played quietly for a period of time. 
  4. User is a fan of the Happy Cake Friends and enjoys playing games or interacting with the Happy Cake Friends brand.

## Design

- #### Site design 
  For a simple, online game, the Happy Cake Friends has a colorful, illustrated look that appeals to those who enjoy a cute, illustrated aesthetic or are fans of the Happy Cake Friends characters or brand. The site design for Happy Cake Friends Memory Game is responsive and the display adjusts responsively across devices.

  The Happy Cake Friends website needed to be responsive and available on a variety of screen sizes and devices to make it as accessible as possible. I focused on the following sizes:

  1. Mobile Device dimensions (small): 280px x 653px
  2. Mobile Device dimensions (larger): 375px and larger
  3. Tablet Device dimensions: 736px and larger
  4. Laptop Device dimensions: 992px and larger

- #### Wireframes
  The Happy Cake Friends website was designed by wireframes with pencil and paper. After sketching out what I planned, I started laying out the HTML and basic CSS for the site in a similar way that the Love Maths tutorial went. I made a list of the functions that I thought that the game would need and proceeded from there. In the end, I did not use different size cards for different levels or different numbers of lives for different levels on this version. I decided to keep it simple and stay with a single version. Difficulty levels can be implemented in a future version of the Happy Cake Friends Memory Game. I recreated the wireframes in a digital version, but an image of the original handdrawn wireframes is included below.

  <details >
  <summary>Mobile Wireframe</summary>  

  ![screenshot of mobile wireframes](docs/documentation/Screenshot_wireframe_mobile.png)
  </details>

  <details >
  <summary>Mobile 375 pexels and larger Wireframe</summary>  

  ![screenshot of mobile wireframes](docs/documentation/Screenshot_wireframe_mobile_lrg.png)
  </details> 

  <details >
  <summary>Desktop Wireframe</summary>  

  ![screenshot tablet wireframes](docs/documentation/Screenshot_wireframe_laptop_desktop.png)
  </details>    

  <details >
  <summary>Original Handdrawn Wireframe</summary>  

  ![screenshot desktop wireframes](docs/documentation/wireframe_memory-game.jpg)
  </details>    
- #### Colour 
  ![screenshot of font family](docs/documentation/screenshot_color_palette.webp)
  The Happy Cake Friends color palette is bright, fresh, and youthful and suits the illustractor Cake Friends characters.
  <br>
  <br>
  Initially, my buttons featured white text and this, in combination with the orange background, failed the acceptable [WCAG](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) contrast ratio. Ultimately, I changed the text color to a dark gray color to ensure readability and accessibility. The Memory Game text was also tested against the blue and green background. At 14 font size and bold, the yellow color was was still readable. So, I chose to leave the colors at the top as is since they text is sufficiently large enough for readability. I used the [Adobe Color](https://color.adobe.com/create/color-contrast-analyzer) to test the colors.

  <details >
  <summary>Adobe color analysis for the button</summary>  

  ![screenshot desktop wireframes](docs/documentation/Screenshot_coloranalysis_yellow-button.png)
  </details> 

  <details >
  <summary>Adobe color analysis for the orange text at the top of the page</summary>  

  ![screenshot desktop wireframes](docs/documentation/Screenshot_coloranalysis_yellow-text-on-blue-background.png)
  </details> 

- #### Typography
  The Happy Cake Friends logo is using the Londrina Solid font family. It offers a cartoon style that works well with the illustrated, cartoon aesthetic of the Happy Cake Friends.

  The remainder of the copy is in the font family is Poppins. It was chosen for it's clean look, readability, and variety of weights. Both fonts were sourced from Google Fonts.

  ![screenshot of font family](docs/documentation/Screenshot_font_poppins.png)
  ![screenshot of font family](docs/documentation/Screenshot_font_londrina-solid.png)


## Features
### Card Grid
<details >
<summary></summary>  

![screenshot card grid](docs/documentation/Screenshot_features_grid.png)
</details>  
The card grid is the main feature of the page and website. Javascript generates the cards on demand when the user presses the "Play" button. The grid is four cards wide and four cards down creating 16 cards total. There are eight matching pairs that are randomly generated each time the card grid is reset. The cards feature the bright and colorful Happy Cake Friends characters.

### Play Button
<details>
<summary></summary>

![screenshot of play button](docs/documentation/Screenshot_features_play-button.png)
</details>
The Play Button is used to begin the game or reset the grid at any time. When a player wins or loses the game, the player can click on the Play Button to reset the game at that time. However, the play button can reset the game at any time and is not limited to the end of the game.

### Player Tries Remaining
<details>
<summary></summary>

![screenshot of player tries](docs/documentation/Screenshot_features_playerTries.png)
</details>
The Player Tries Remaining section displays the current tries that a player has as they attempt matches. At the beginning, each player is allocated 15 Tries or attempts. Each mismatched pair decrements the Player Tries by 1 until it reaches 0. At this point, a message pops up to let the player know that they have lost the game and they can play again if they choose.

### Win Game and Lose Game Modals
<details>
<summary></summary>

![screenshot of win game modal](docs/documentation/Screenshot_features_modals.png)
</details>
The Player Tries Remaining section displays the current tries that a player has as they attempt matches. At the beginning, each player is allocated 15 Tries or attempts. Each mismatched pair decrements the Player Tries by 1 until it reaches 0. At this point, a message pops up to let the player know that they have lost the game and they can play again if they choose. Should the player find all the matches before the Player Tries reaches zero. Then, they have won the game and a Win Game message pops up at that time. They can also choose to play the game again at this point.


### Footer
<details>
<summary></summary>

![screenshot of footer](docs/documentation/Screenshot_features_footer.png)
</details>
The footer section features a simple copyright message for the Happy Cake Friends. 

### Favicon
<details >
<summary></summary>  

![screenshot favicon](docs/documentation/Screenshot_favicon.png)
</details>  
A favicon was added to provide further visual support of the Happy Cake Friends brand.

### 404 Page Not Found page
<details >
<summary></summary>  

![screenshot favicon](docs/documentation/Screenshot_features_404page.png)
</details>  
In the event that the user navigates to non-existing page, a 404 page displays a Page not Found message and directs the user back to the main game page.


## Future Features
- A future feature would be allow for different levels or different numbers of tries to increase or decrease difficulty.
- A future feature would allow for different character groups to displayed depending on the level of difficulty.
- Also for future development, additional simple games featuring the characters. 

## Technologies
  ### Languages Used
  - HTML5
  - CSS
  - Javascript

  ### Technologies and Programs Used
  - GitHub - used to save and store all the files for this website
  - GitHub Codespaces - was used as the IDE to develop and test the code for this website
  - Git - provided the version control
  - Adobe Photoshop 2024 - used to create wireframes and edit all the images
  - Wacom One: creative pen display and pen tablet
  - Google Docs - used for notes and documentation
  - Google Fonts - imported fonts from this website
  - Google Developer Tools - used to debug website and test for responsiveness
  - Google Lighthouse - used to audit the performance and quality of the website
  - WC3 HTML Validator - used to validate the HTML code
  - WC3 CSS Validator - used to validate the CSS code https://jigsaw.w3.org/css-validator/
  - JShint.com Javascript Validator - used to validate the Javascript code https://jshint.com/

  ### Deployment
  GitHub was used to deploy this website. The following steps were taken:

  1. Log into GitHub account.
  2. Navigate to the project repository: [Memory-game](https://github.com/hysinh/Memory-game?)
  3. Click on the Settings button on the horizontal navigation across the top portion of the page.
  4. Navigate to the Pages link under the Code and automation section on the left navigation.
  5. Under GitHub Pages, go to Build and deployment. Then, under Source, select "Deploy from a branch". 
  6. Next, under Branch, select "main" and "/root" and then click on the Save button.
  7. After a few moments, the website will be made live and the link will be made visible at the top of the page. 

  How to clone the Happy Cake Friends Memory Game & make changes:
  1. Open the [Memory-game repository](https://github.com/hysinh/Memory-game?) on GitHub.
  2. Navigate to the CODE link on the navigation across the top.
  3. Then, navigate to the green CODE button on the right side and click.
  4. Select the Local tab and click on the copy icon to make a copy of the repository.
  5. Then navigate back to your main GitHub dashboard and then create a new repository with your desired name.
  6. On the next page, navigate to the bottom of the page and select Import code under "Import code from another repository".
  7. In the next window, paste the copied link of the [Memory-game repository](https://github.com/hysinh/Memory-game?) into the line.
  8. Then, click Begin Import to import the repository code.
  9. Make changes and/or deploy as desired.



  ## Testing

  ### Validator Testing
  - #### HTML Validation
    No errors were returned when passing the official W3C HTML Validator
    <details >
    <summary>Index Page HTML Validation</summary>  

    ![screenshot of index page validation](docs/documentation/Screenshot_htmlvalidator.png)
    </details>

    <details >
    <summary>404 Page HTML Validation</summary>  

    ![screenshot of index page validation](docs/documentation/Screenshot_htmlvalidator_404.png)
    </details>
     
    
  - #### CSS Validation
    No errors were found when passing through the official W3C CSS Jigsaw validator
    <details >
    <summary>Index Page CSS Validation</summary>  

    ![screenshot of css validation](docs/documentation/Screenshot_cssvalidator.png)
    </details>

    <details >
    <summary>404 Page CSS Validation</summary>  

    ![screenshot of css validation](docs/documentation/Screenshot_cssvalidator_404.png)
    </details>

  - #### Javascript Validation
    No errors were found when passing through the JSHint Javascript validator
    <details >
    <summary>Javascript Validation</summary>  

    ![screenshot of css validation](docs/documentation/Screenshot_jshint_jsvalidator.png)
    </details>

  
  - #### Lighthouse Performace Audit via Chrome Dev Tools
    Desktop Lighthouse Performance Audits
    <details >
    <summary>Index Page Lighthouse audit</summary>  

    ![screenshot of index page lighthouse audit](docs/documentation/Screenshot_lighthouse_desktop.png)
    </details>

    <details >
    <summary>404 Page Lighthouse audit</summary>  

    ![screenshot of 404 page lighthouse audit](docs/documentation/Screenshot_lighthouse_desktop_404.png)
    </details>
    
    <br>

    Mobile Lighthouse Performance Audits
    <details >
    <summary>Index Page Lighthouse audit</summary>  

    ![screenshot of index page lighthouse audit](docs/documentation/Screenshot_lighthouse_mobile.png)
    </details>

    <details >
    <summary>404 Page Lighthouse audit</summary>  

    ![screenshot of 404 page lighthouse audit](docs/documentation/Screenshot_lighthouse_mobile_404.png)
    </details>

  ### Manual Testing
  Manual testing was performed on the website checking for broken links, content errors, and responsivity across different sizes. Testing took place during the build process using Dev Tools on Chrome and on the following real-world devices and browsers:

  #### Devices 
  1. Pixel 4XL
  2. Xiaomi 11T Pro
  3. Redmi Note 12 Pro+
  4. Lenovo IdeaPad Y500 Laptop
  5. Alienware Aurora R7 Desktop
  6. Microsoft Surface

  #### Browsers
  1. Microsoft Edge
  2. Brave
  3. Google Chrome
  4. Opera

  #### The results of testing are as follows:
  | Page | Test | Pass/Fail |
  | ---- | ---- | --------- |
  | Home  | Happy Tree Friends logo links back to the homepage | Pass |
  | Home  | Images and sections are responsive to different device sizes | Pass |
  | Home  | Play button works on click and sets the card grid correctly | Pass |
  | Home  | If the user clicks on a card, it flips to display the card. The card cannot be clicked to flip it back. | Pass |
  | Home  | If the user clicks on a second card, it flips to display the card. The two flipped cards are compared. If they match, the user is allowed to click on a new card. If they don't match, the cards will reset and the user can click on a new card (or one of the ones that didn't match). | Pass |
  | Home  | If the user find all the matches, the matches are validated and user receives a Win message. | Pass |
  | Home  | If the user exhausts their player tries before finding all the matches, the board is locked and the user receives a Lose message. | Pass |
  | Home  | If the user receives a Lose or Win message, when they click on the screen, the modal closes and they can reset the game if they choose. | Pass |
  | 404  | Page displays when user attempts to go to a non-existing page | Pass |
  | 404  | Link on the page bring user back to the home page | Pass |

  #### Bugs and Fixes
  | Bug | Page | Fix |
  | --- | ---- | --- |
  | Can still click on cards after lose game | Index page | Added a lockBoard function in JS file to resolve. |
  | Can still click on a third card when two first cards are being compared | Index page | Change < 2 in checkCards function to === 2 to prevent a third card from being flipped | 
  | When the user completes a game but lost, user can click several times on a card and it will eventually flip over | Index page | Added a lockBoard function to the checkLose function in JS file to resolve. |
  | Missing h2 close tag | Index page | Had changed an H1 tag to a H2 tag but did not update the close tag. Resolved by updating close tag. |
  | Section element | Index page | HTML validator suggested changing section element to div to eliminate issues with lack of heading. I changed the section element to a div element. |
  | Accessibility | Index page | Document doesn't use legible font sizes at the mobile size in the footer. The footer text size was adjusted to ensure better readability |
  | Invalid 'align' property | style.css | Removed align property  |
  | Unnecessary ; tags | script.js | I had put ; at the end of every function that was unncessary. Resolved by removing them. |
  | Missing ; tags | Script.js | Missing ; at the end of console.log in js file in two places. Added the ; as necessary. |
  

  ### Unfixed Bugs
  - At this time, because the cards all are added as elements to the DOM, it is possible to cheat by viewing the html source. You are able to see each image and it's names and it's location. I do not have enough programming knowledge at this time to avoid this.
  

## Credits
### Content
- Content for website was writing by myself
- Jason Holt Smith, https://github.com/bicarbon8, was available for copious amounts of assistance debugging and helping to steer me in the correct direction for writing the code.
- Grid layout https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
- Modal code https://codepen.io/dantewebmaster/pen/Yabpmr
- W3C CSS Validator: https://jigsaw.w3.org/css-validator/
- How to randomize the array: The de-facto unbiased shuffle algorithm is the Fisher–Yates (aka Knuth) Shuffle. https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
- How to Make a Modal https://www.w3schools.com/howto/howto_css_modals.asp
- How to use docstrings in Javascript https://stackoverflow.com/questions/34205666/utilizing-docstrings
- Build Your Own Memory Card Game with HTML, CSS, and JavaScript - Beginner-Friendly Tutorial https://www.youtube.com/watch?v=xWdkt6KSirw
- Awesome Vanilla JavaScript Memory Card Game Tutorial https://www.youtube.com/watch?v=-tlb4tv4mC4
- How to toggle https://developer.mozilla.org/en-US/docs/Web/API/Element/classList & https://www.w3schools.com/howto/howto_js_toggle_class.asp
- How to stack div elements vertically https://stackoverflow.com/questions/19284923/how-do-i-automatically-stack-divs-vertically-inside-a-parent
- How to remove a class from an element https://www.w3schools.com/howto/howto_js_remove_class.asp
- How to set multiple conditions in an if statement in JavaScript https://www.shecodes.io/athena/132703-how-to-set-multiple-conditions-in-an-if-statement-in-javascript#:~:text=In%20JavaScript%2C%20you%20can%20set



### Media
- Artwork was created by myself on Adope Photoshop
- The Happy Cake Friends characters were created by my daughter, Liloux Smith. They were redrawn in Adobe Photoshop for the purposes of this project.