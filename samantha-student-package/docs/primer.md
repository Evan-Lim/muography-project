# A short primer on muography

*Read sections 1–2 in week 1, section 3 in week 2, and sections 4–5 before you
start notebook 04. Nothing here needs mathematics beyond Form 4, and where a
formula appears it is explained in words first.*

---

## 1. Where muons come from

Somewhere in the galaxy — a supernova remnant, most likely — a proton is
accelerated to an absurd energy and begins a journey that ends above your head.
When it strikes a nucleus in the upper atmosphere, roughly 15 km up, it shatters
it. The debris includes short-lived particles called pions, and pions decay
almost immediately into **muons**.

A muon is, for our purposes, a heavy electron. Same charge, same lack of
internal structure, but about 207 times the mass. That extra mass is the entire
reason muography is possible, and we will come back to it.

Muons are unstable. Left alone, a muon lives about 2.2 microseconds before
decaying. Light travels only 660 m in that time, so by the naive calculation
almost none should reach the ground from 15 km up. They arrive anyway, in
enormous numbers, because they are moving so close to the speed of light that
time runs slowly for them — this is special relativity, and cosmic-ray muons at
sea level are among the most direct everyday evidence that Einstein was right.

The number to carry in your head:

> **About 10,000 muons pass through every square metre of the ground every
> minute**, arriving mostly from overhead.

At sea level, looking straight up, the flux above 1 GeV is roughly 60–70 muons
per square metre per second per steradian. You will reproduce that number in
notebook 01.

Two features of the arriving muons matter for us.

**They come from all directions, but not equally.** The flux falls off roughly
as cos²θ away from the vertical. Muons arriving at a slant have crossed more
atmosphere, and more of them have been absorbed or decayed on the way.

**They span an enormous range of energies.** Most are a few GeV. A small
fraction are hundreds of GeV. A very few exceed 10,000 GeV. That tail is what
makes imaging thick objects possible: only the rare, very energetic muons get
through a mountain, and there are just barely enough of them.

---

## 2. Why muons go through rock

Charged particles lose energy as they pass through matter, mostly by knocking
electrons off the atoms they pass. The rate of loss depends on how much matter
is in the way — not on what kind. This is why physicists measure thickness in a
strange-looking unit:

**Opacity** = density × path length, in grams per square centimetre.

One metre of limestone (density 2.5 g/cm³) is 250 g/cm². One metre of water is
100 g/cm². A muon does not much care which of those it crosses; it cares about
the number of grams per square centimetre.

The energy loss rate is about **2 MeV per g/cm²** at moderate energies. So:

- crossing 1 m of limestone costs a muon about 0.5 GeV,
- crossing 100 m costs about 50 GeV,
- crossing 500 m costs several hundred GeV, and by then a second mechanism
  (radiation) has begun to matter as well.

Now the key comparison. An electron with the same energy would have been stopped
almost immediately, because a light particle radiates energy violently when it
is deflected. A muon, being 207 times heavier, radiates 207² ≈ 43,000 times less
readily. It simply keeps going. This is why muons, and not electrons, are the
particle that can see inside a mountain.

Meanwhile a proton or an alpha particle, though also heavy, feels the strong
nuclear force and is absorbed by the first nucleus it meets. The muon does not
feel the strong force at all.

So the muon occupies a unique niche: heavy enough not to radiate, blind to the
strong force, abundant, and free. There is no substitute for it in nature.

---

## 3. How this becomes an image

Here is the whole method in four sentences.

1. Point a detector at a target and count how many muons arrive from each
   direction.
2. Directions with more material in the way deliver fewer muons.
3. Compare what you counted to what you would have counted if the target were
   uniformly solid.
4. Wherever you counted *more* muons than expected, there is less material than
   expected — a cavity.

This is a shadow image, in exactly the sense of a medical X-ray, with one
difference: the source is the sky, it is always on, it is free, and nobody can
turn it off or aim it. You cannot choose your beam. You can only choose where to
put the detector and how long to wait.

### The most famous result

In November 2017 a collaboration led by Kunihiro Morishima published the
discovery of a large void inside the Great Pyramid of Khufu, at least 30 m long,
above the Grand Gallery. It had been sealed and unseen for about 4,500 years.
Three independent detector technologies — nuclear emulsion films, scintillator
hodoscopes, and gas detectors — all saw the same excess of muons.

Nobody drilled anything. The pyramid was never touched. That is the appeal of
the method, and it is why the same technique is now used to watch magma move
inside volcanoes, to check the concrete inside ageing bridges and tunnels, to
search for cavities under roads before they collapse, and to look for uranium
inside the ruins of the Fukushima reactors, where no human can go.

Your project is a simulation of exactly this measurement.

---

## 4. Why it takes so long

Here is the catch, and it is the reason your project has a research question
rather than just a picture.

Under 100 m of limestone, the surviving muon flux is roughly 0.4 per square
metre per second per steradian. A small detector, 0.25 m² in area, looking at a
patch of sky 2° across, collects:

    0.4  x  0.25 m²  x  0.0012 sr  x  86400 s  ≈  10 muons per day

Ten. Not ten thousand. Ten.

And a cavity might change that number by 30%, meaning 13 muons instead of 10.
After one day, would you believe that difference? Of course not — you would get
13 muons instead of 10 quite regularly by pure chance.

This is why muography experiments run for months.

---

## 5. Counting statistics, and what "5 sigma" means

When events arrive at random at a steady average rate, the number you count in a
fixed time follows a **Poisson distribution**. It has one property you need:

> If you expect *N* events, a typical measurement lands within about **√N** of
> *N*.

Expect 100, get 100 ± 10 — a 10% uncertainty.
Expect 10,000, get 10,000 ± 100 — a 1% uncertainty.

Notice what that means. Counting for ten times longer gives you ten times the
muons, but only √10 ≈ 3.2 times the precision. **Precision improves as the
square root of time.** Doubling the significance requires four times the exposure, because significance grows as the square root of time.
This single fact governs the design of every muography campaign ever run.

To describe an excess, this project uses two closely related quantities.

**Expected significance** uses two expectation values:

    expected significance = (expected with cavity − expected without cavity) / √(expected without cavity)

It is deterministic for fixed project parameters and defines the smooth exposure
curve used for the headline result.

**Observed significance** instead uses one noisy Poisson count map:

    observed significance = (observed − expected without a cavity) / √(expected without a cavity)

It changes when the random seed changes. The noisy value should fluctuate around
the expected curve; it is not the definition of the official exposure time.

- **1σ** — happens about one time in three. Meaningless.
- **3σ** — about one time in 750. Interesting; worth another look.
- **5σ** — the stringent benchmark used for this project. Here it is a predefined
  simulation threshold, not a complete real-world discovery test.

Why such a severe bar? Because you are not testing one pixel. Your image has
1,681 of them. If each pixel has a 1-in-750 chance of faking a 3σ signal, then
in a pure-noise image you should *expect* two or three pixels at 3σ. They can look like a signal, even though they are nothing more than statistical noise.

This effect has a name — the *look-elsewhere effect* — and it has embarrassed
serious physicists more than once. In notebook 04 you will demonstrate it for
yourself by running your own analysis on a pyramid you know to be solid, and
seeing what the noise alone can produce.

---

## 6. What is left out

Your simulation is honest about the physics that dominates, and silent about
several things a real experiment must handle. Knowing what you have left out is
part of understanding what you have built, and it belongs in your report.

- **Muon scattering.** Real muons do not travel in perfectly straight lines;
  they are deflected slightly by every nucleus they pass. This blurs real images.
- **Detector imperfection.** Real detectors miss some muons, mis-measure the
  direction of others, and occasionally record particles that were never muons
  at all.
- **Background.** Some particles reaching the detector are not muons that
  crossed the target — electrons from local radioactivity, or muons scattered in
  from outside. Real analyses spend enormous effort removing these.
- **Knowing the rock.** We assumed we know the density of the limestone exactly.
  In reality, an unexpected cavity and slightly-lighter-than-expected rock look
  identical to a muon.

That last one is the deepest limitation of the method, and it is worth a
sentence in your discussion. Muography measures *density along a line*. Turning
that into a statement about a chamber always requires an assumption about
everything else.

---

## 7. If you want to read further

Start with the Khufu discovery paper. It is in *Nature*, it is short, and the
figures will look reassuringly familiar once you have finished notebook 04:

> Morishima, K. et al. "Discovery of a big void in Khufu's Pyramid by
> observation of cosmic-ray muons." *Nature* **552**, 386–390 (2017).

Then, for the field as a whole:

> Bonomi, G., Checchia, P., D'Errico, M., Pagano, D., Saracino, G. "Applications
> of cosmic-ray muons." *Progress in Particle and Nuclear Physics* **112**,
> 103768 (2020).

And for the physics of the muon flux itself, the Particle Data Group's review of
cosmic rays is the standard reference that essentially every paper in the field
cites. It is freely available online.

None of these are written for secondary-school students, and you should not
expect to understand every line. Read them the way researchers actually read
papers: the abstract, then the figures, then the conclusions, then back to
whichever paragraph now seems worth the effort.
