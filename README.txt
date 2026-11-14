begwork website
===============
plain static site, deliberately ugly: default fonts, no css, pictures pasted at random sizes.

  index.html      the page (all the js is at the bottom of it)
  config.js       ca + links + picture lists  <- the only file you normally edit
  sync_assets.py  copies the art into img/ and rewrites the picture lists
  img/            main.png, pfp.png, banner.png, favicon.png, memes/, stickers/

preview: double click index.html.


1. before launch
----------------
leave CA as "" in config.js. the site then shows "ca drops at launch" and the
buy / dexscreener buttons are greyed out with "(soon)". same for any empty link.


2. after launch: fill config.js
-------------------------------
open config.js in notepad and paste between the quotes:

  CA: "the pump.fun mint address",
  X_URL: "https://x.com/<the begwork account>",
  TG_URL: "https://t.me/<the group>",
  STICKERS_URL: "https://t.me/addstickers/<the pack name>",

buy (https://pump.fun/coin/<CA>) and dexscreener (https://dexscreener.com/solana/<CA>)
links are built from CA automatically. save, then re-deploy (step 5).


3. update the pictures
----------------------
whenever begwork/memes/*.png or begwork/stickers/*.png change, run:

  python sync_assets.py

it copies begwork/memes/*.png -> img/memes/, begwork/stickers/*.png -> img/stickers/,
begwork/main.png, pfp.png, banner.png -> img/, remakes img/favicon.png (64x64 from pfp.png)
and rewrites the memes / stickers lists in config.js (between the "// memes start/end"
and "// stickers start/end" markers; dont delete those lines). it needs python 3 + pillow.
pngs removed from the source folders are removed from img/ too. gallery order = filename order.


4. link previews (og:image)
---------------------------
x / telegram / discord only show the banner if og:image and twitter:image are FULL urls.
after you know the address, open index.html and change both

  <meta property="og:image" content="img/banner.png">
  <meta name="twitter:image" content="img/banner.png">

to e.g.  content="https://begwork.xyz/img/banner.png"   (your real address).
optionally add  <meta property="og:url" content="https://begwork.xyz/">
check it by pasting the link into a telegram chat or into https://www.opengraph.xyz


5. online now: https://realdoomsman.github.io/begwork/
-------------------------------------------------------
hosted on github pages, repo github.com/realdoomsman/begwork (this folder is that repo).
to update after editing config.js or running sync_assets.py, in this folder run:
  git add -A && git commit -m "update" && git push
the live site refreshes about 30 seconds later.

other free hosts if you ever move it:
netlify drop (easiest, no account needed to try):
  go to https://app.netlify.com/drop and drag the whole "site" folder onto the page.
  you get a https://something.netlify.app address. make a free account to keep it
  and to update it later (Deploys -> drag the folder again).

vercel:
  npm i -g vercel, then inside the site folder run: vercel --prod
  (or import a github repo at https://vercel.com/new, framework preset "Other").

github pages:
  make a public repo, upload the contents of the site folder (index.html at the top level),
  Settings -> Pages -> Deploy from branch -> main / root. address: https://<user>.github.io/<repo>/

the site_shots folder next to this one is just test screenshots. dont upload it.


6. connect a domain
-------------------
buy the domain anywhere (namecheap, porkbun, cloudflare...). then:
  netlify: Site configuration -> Domain management -> Add a domain, follow the dns records it shows
           (usually an A record to 75.2.60.5 or a CNAME to <site>.netlify.app).
  vercel:  Project -> Settings -> Domains -> Add, copy the A / CNAME records it shows.
  github pages: Settings -> Pages -> Custom domain, then a CNAME record pointing to <user>.github.io.
https is automatic on all three after dns updates (minutes to a few hours).
then redo step 4 with the new address.


not financial advice. just begging.
