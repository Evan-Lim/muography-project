<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Simulation Study of Exposure Time and Systematics for Cosmic-ray Muography for Hidden Chambers</h3>

  <p align="center">
    Under a simulation model, how long would a 0.25 m² detector observing the baseline pyramid need before the expected chamber signal reaches 5σ?
    <br />
    <a href="https://github.com/Evan-Lim/muography-project"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Every minute, about ten thousand cosmic-ray muons pass through every square metre of the ground you are standing on. They come from the deaths of stars, they arrive at nearly the speed of light, and they are heavy enough to travel through hundreds of metres of solid rock before stopping.

That last fact makes them useful. Count how many muons emerge from a mountain from many viewing directions, and you can work out what is inside it — without drilling, without touching it, without ever going in. In 2017 a team used exactly this method to find a chamber inside the Great Pyramid of Khufu that had been sealed for four and a half thousand years.

This project builds a working simulation of that measurement, and use it to answer a question with a number:

> **Under this simulation model, how long would a 0.25 m² detector observing the baseline pyramid need before the expected chamber signal reaches 5σ?**

The headline number is an expected sensitivity of the simulated setup, not an automatic prediction for a real detector. Individual noisy simulations will fluctuate around it.

Here's a blank template to get started. To avoid retyping too much info, do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`, `project_license`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Getting Started -->
## Installation

```bash
pip install -r requirements.txt
jupyter notebook
```

Then open `notebooks/00_start_here.ipynb` and work through it. Read
`docs/primer.md`.

If `import muography` fails, you probably skipped the first setup cell. Every
notebook adds `code/` to its Python path automatically; run that cell first.

For notebooks 03–05, the functions come from `code/student_analysis.py`,
so those notebooks can be restarted and run independently.

## How the notebooks work

Each contains three kinds of cell: **explanation** (read it), **given code**
(run it), and **`# YOUR TURN`** (write it). The `YOUR TURN` cells are the
project. Where a cell says *check yourself*, there is a number you should be
able to reproduce.

| Notebook | Weeks | What it contains |
|---|---|---|
| `00_start_here` | 1 | Setup and a numpy warm-up |
| `01_muons_and_rock` | 1–2 | The muon spectrum; how much energy it takes to cross rock |
| `02_ray_tracing` | 3–4 | A virtual pyramid, and a map of how much rock lies in every direction |
| `03_first_image` | 5 | Expected muon counts, and dividing out the shape of the pyramid |
| `04_noise_and_exposure` | 5–6 | Random noise, significance, and **the headline result** |
| `05_parameter_study` | 6–7 | What makes a chamber easy or hard to find |


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Contributors:

<a href="https://github.com/Evan-Lim/muography-project">
  <img src="https://contrib.rocks/image?repo=Evan-Lim/muography-project" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Junyi Chai - 

Evan Lim Hong Yan - 

Samantha Chan Teng Wei - chantengwei@gmail.com

Project Link: [https://github.com/Evan-Lim/muography-project](https://github.com/Evan-Lim/muography-project)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
<!-- Shields.io badges. You can a comprehensive list with many more badges at: https://github.com/inttter/md-badges -->
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
