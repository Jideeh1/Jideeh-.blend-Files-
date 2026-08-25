# Jideeh's `.blend` Files!

<p align="center">
  <img src="/.Media/Thumbnail.png">
</p>

> [!IMPORTANT]
> All other models require Goo Engine 4.1.1 or later.
> Script names must not be changed!

---

<p align="center">
    <a href="https://github.com/Jideeh1/Jideeh-.blend-Files-/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Jideeh1/Jideeh-.blend-Files-?style=for-the-badge"></a>
    <a href="https://discord.gg/85rP9SpAkF"><img alt="Discord" src="https://img.shields.io/discord/894925535870865498?style=for-the-badge"></a>
    <a href="https://github.com/Jideeh1/Jideeh-.blend-Files-/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/Jideeh1/Jideeh-.blend-Files-?style=for-the-badge"></a>
</p>

---

## How to Download

The Entire Repository:

1. Click the green **Code** button.
2. Click **Download ZIP**.
3. Extract the ZIP file.

A single File:

<p align="center">
  <img src="/.Media/Download Tutorial.gif">
</p>

# Setup your own models! 
FOLLOW THESE EXACT INSTRUCTIONS if you want to setup your own models using the new setup file.
1. You NEED to use models from <https://cdn.hoyotoon.com/s/assets>
2. Install BetterFBX (needs to be 5.2) and Expykit or download the addons in this repository.
3. Open the goo blend file `Setup File.blend`.
4. Under the item tab, there should be a panel called "Jideeh Script Runner" with exactly THREE  buttons. Click the **"Better FBX Importer"** and import your model. **THE FBX, MATERIALS, AND TEXTURE HAS TO BE IN THE SAME FOLDER.**
5. After importing the model, click the 2nd button **"Rig, Outline, Shaders."**
Check here to see what it does.
6. **Conditional:** if the model uses the wrong face lightmap/has no face lightmap, use the 2nd panel in the item tab called **"Face Lightmap Switcher"** (If you don't see it, check the scripting tab and run it.) This lets you add or switch lightmaps with one button.
7. **Optional:** Click **"Jideeh's Setup."**

Credits to the lovely people here who have made the ZZZ setup file. https://discord.com/channels/894925535870865498/1439443691142910077, and credits to @jrdan_ & @starriia for teaching me how to setup models. Give their repositories lots of love! [Star's Repository](<https://github.com/starriia/stars-blend-files>) | [Jordan's Repository](<https://mega.nz/folder/27hnRR6Q#JbVN0z1hKitbKq-6R0dOlg>).

## Top-level buttons
 
These sit at the top of the panel and are always visible.
 
| Button | Operator | What it does |
|--------|----------|--------------|
| **BetterFBX** | `jideeh.run_better_fbx_importer` | Opens the BetterFBX importer file dialog. It probes a list of known BetterFBX operator IDs and invokes the first one that exists, so it keeps working across BetterFBX versions. If none is found, it raises an error telling you to check the operator name in the Info log. |
| **Rig, Outline, Shaders** | `jideeh.run_setup_shader_rig_outline` | Runs the text block named `#1 Setup shader, rig, and outline` — the main one-shot setup that builds the body rig, outlines, and shaders for a character. |
| **Jideeh's Setup** | `jideeh.run_jideeh_setup` | Runs the text block named `Jideeh's Setup` — your personal follow-up/setup pass. |
 
---
 
## Extra Utilities (collapsible)
 
Expanded via the **Extra Utilities** sub-panel header. Grouped into three labeled rows.
 
### Rigs
 
| Button | Operator | What it does |
|--------|----------|--------------|
| **Bangboo** | `jideeh.run_bangboo_rig` | Runs the `Bangboo Rig` text block (Bangboo companion rig generator). |
| **Thugs** | `jideeh.run_thugs_rig_script` | Runs the `Thugs Rig Script` text block (rig generator for the "thug"/NPC humanoid characters). |
| **Facerig** | `jideeh.run_facerig` | Runs the `Facerig` text block — the ZZZ/HSR-style NPR face rig generator. |
 
### Shaders & Outlines
 
| Button | Operator | What it does |
|--------|----------|--------------|
| **With Face** | `jideeh.run_shaders_outlines` | Runs the `Shaders & Outlines` text block — applies shaders and outlines including the face material. |
| **No Face** | `jideeh.run_shaders_outlines_no_face` | Runs the `Shaders & Outlines No Face` text block — same, but skips the face (for characters where the face is handled separately). |
 
### Fixes
 
| Button | Operator | What it does |
|--------|----------|--------------|
| **Face Panel** | `jideeh.run_face_panel_controllers` | Runs the `Face Panel Controllers` text block (builds/repairs on-screen face panel controllers). |
| **Remove Empties** | `jideeh.run_remove_empties` | Runs the `Purge Empties` text block — cleans up leftover Empty objects from import. |
 
---
 
## Face Lightmap toggle (collapsible)
 
Expanded via the **Face Lightmap toggle** sub-panel header. This section swaps the face lightmap texture used by the `ZZZ Shader Face` material on whatever mesh ends in `_Face`.
 
The available slider groups are built from `LIGHTMAP_GROUPS`. The **Monster** group is pulled out and given its own button; all other groups become sliders.
 
| Control | Type | What it does |
|---------|------|--------------|
| **Female** | Slider (1–3) | Cycles between the three Female face lightmaps (`Female_Face_Lightmap.png`, `_02`, `_FX`). Changing the value immediately swaps the lightmap image node(s) in the face material. |
| **Male** | Slider (1–2) | Cycles between the two Male face lightmaps. |
| **NPC Face** | Slider (1–2) | Cycles between the Child and Older NPC face lightmaps. |
| **NPC Furry** | Slider (1–3) | Cycles between the three NPC Furry face lightmaps. |
| **Monster** | Button | Sets the face lightmap directly to `Monster_Face_01_Lightmap.png` (the Monster group has only one map, so it's a button instead of a slider). |
 
Each slider finds the face lightmap image node(s) inside the material node tree (recursing through group nodes, matching by name/label/`Face Lightmap` group) and re-points them at the selected image. If it can't find a face mesh, a matching material slot, or the lightmap node, it reports which nodes it *did* find so you can diagnose the mismatch.
 
---
 
## Face FX (collapsible)
 
Expanded via the **Face FX** sub-panel header. This section manages the "Face FX" mesh/material setup (blush, Aozameru, etc.) transplanted from an external `.blend` file.
 
| Button | Operator | What it does |
|--------|----------|--------------|
| **Get Face FX Mesh** | `jideeh.append_face_fx` | Opens a `.blend` file browser and appends the **Face FX** collection (and the `Face Effect` material) from it. It transplants the appended `Face Effect` material into `ZZZ Shader Face` via `user_remap` + rename, tags the Face FX collection with a color, excludes the `WGTS` widget collection from the view layer, inserts the **Face Lightmap** node before the Separate Color node, and fills in the `_Face_D` diffuse texture. If **Cache** is on and a cached path exists, it skips the file dialog and reuses that path. |
| **Apply Drivers** | `jideeh.apply_face_fx_drivers` | Full first-time setup: creates the custom properties on the `_Face` mesh (`Aozameru`, `Aozameru Top to Down`, `Blush Color`, `Blush Type`, `OG Aozameru Intensity`, `OG Blush Intensity`, `Switch FX`), removes obsolete old properties, wires up all the AVERAGE-type drivers from those properties to the shader node sockets, assigns the Face FX widget armature bones into the `Facerig` bone collection, re-fills the face texture, and refreshes. Reports any drivers it had to skip. |
| **Refresh** | `jideeh.refresh_face_fx` | Lightweight refresh — tags the `ZZZ Shader Face` material and its node tree for update and re-sets the current frame, to shake loose stale driver/depsgraph evaluation. Does not rebuild anything. |
| **Rebuild** | `jideeh.rebuild_face_fx` | Re-wires the Face FX drivers on the existing `_Face` mesh **without** recreating the custom properties, then refreshes. Use this when the properties already exist but the driver links broke. Reports skipped drivers. |
| **Parent Face Mesh** | `jideeh.parent_face_mesh` | Parents the appended `Face FX` mesh to the character rig (armature ending in `Rig`), zeroes its shape keys, adds all its verts to the `DEF-spine.006` vertex group so it follows the head, joins it into the main `_Face` mesh, and hides the `Face Expressions` bone. |
 
### Cache row
 
| Control | Type | What it does |
|---------|------|--------------|
| **Cache** | Checkbox | When enabled, remembers the last Face FX `.blend` path so **Get Face FX Mesh** skips the file dialog and reuses it. |
| **Clear** (trash icon) | `jideeh.clear_face_fx_cache` | Clears the stored Face FX cache path, forcing the file dialog to appear again next time. |
 
---
 
## Notes
 
- **Text-block dependency:** every "run" button (`BetterFBX` is the exception — it calls an operator) looks up a named text block and `exec`s it. The names it looks for are defined at the top of the file (`SCRIPT_1_TEXT_NAME` … `SCRIPT_9_TEXT_NAME`). It matches with or without a `.py` extension, and errors out with a list of available text blocks if the target is missing.
- **Auto Keying** is force-disabled around every action and again at registration.
- **Auto-register:** on run, the script scans all text blocks for its own operator markers and flags the matching one as a module so it re-registers automatically on file load.
# Model List

## Playable (97)

| # | Model | # | Model | # | Model |
|---|-------|---|-------|---|-------|
| 1 | [Alexandrina/Rina](https://discord.com/channels/894925535870865498/1521444394576642118/1528584224230342677) | 34 | [Ellen Joe on Campus](https://discord.com/channels/894925535870865498/1521444394576642118/1539517414361014304) | 67 | [Remielle Dan Swimwear](https://discord.com/channels/894925535870865498/1521444394576642118/1538579604153827478) |
| 2 | [Alice](https://discord.com/channels/894925535870865498/1521444394576642118/1537607892851630080) | 35 | [Evelyn Chavelier](https://discord.com/channels/894925535870865498/1521444394576642118/1528617660529643530) | 68 | [Rose Pryce](https://discord.com/channels/894925535870865498/1521444394576642118/1532990443535728790) |
| 3 | [Alice Swimwear](https://discord.com/channels/894925535870865498/1521444394576642118/1528585895698239608) | 36 | [Grace Howard](https://discord.com/channels/894925535870865498/1521444394576642118/1528617933826293800) | 69 | [Seth](https://discord.com/channels/894925535870865498/1521444394576642118/1528643211827089450) |
| 4 | [Anby](https://discord.com/channels/894925535870865498/1521444394576642118/1528588773930176553) | 37 | [Hoshimi Miyabi](https://discord.com/channels/894925535870865498/1521444394576642118/1539518732747931658) | 70 | [Seed](https://discord.com/channels/894925535870865498/1521444394576642118/1532254546703945768) |
| 5 | [Soldier 0 Anby](https://discord.com/channels/894925535870865498/1521444394576642118/1528589105544564768) | 38 | [Hoshimi Miyabi Dignified Blossom](https://discord.com/channels/894925535870865498/1521444394576642118/1528618561398898758) | 71 | [Sigrid](https://discord.com/channels/894925535870865498/1521444394576642118/1528643645123723335) |
| 6 | [Anton](https://discord.com/channels/894925535870865498/1521444394576642118/1528589670856917122) | 39 | [Hugo Vlad Old](https://discord.com/channels/894925535870865498/1521444394576642118/1528619291266650142) | 72 | [Sigrid Swimwear](https://discord.com/channels/894925535870865498/1521444394576642118/1528643874749288569) |
| 7 | [Aria](https://discord.com/channels/894925535870865498/1521444394576642118/1528590187276275762) | 40 | [Hugo Vlad New](https://discord.com/channels/894925535870865498/1521444394576642118/1528619588089020546) | 73 | [Soldier 11](https://discord.com/channels/894925535870865498/1521444394576642118/1528644185756798976) |
| 8 | [Aria Robot Form](https://discord.com/channels/894925535870865498/1521444394576642118/1539497994359939073) | 41 | [Jane Doe](https://discord.com/channels/894925535870865498/1521444394576642118/1539519262350250015) | 74 | [Soukaku](https://discord.com/channels/894925535870865498/1521444394576642118/1528644474203541594) |
| 9 | [Aria Robot Form Discordant Note](https://discord.com/channels/894925535870865498/1521444394576642118/1539499613797486624) | 42 | [Jane Doe Nocturne of Light](https://discord.com/channels/894925535870865498/1521444394576642118/1539519545134551070) | 75 | [Trigger](https://discord.com/channels/894925535870865498/1521444394576642118/1528644741305077790) |
| 10 | [Aria Discordant Note](https://discord.com/channels/894925535870865498/1521444394576642118/1528688359243776020) | 43 | [Ju Fufu](https://discord.com/channels/894925535870865498/1521444394576642118/1539520289761665065) | 76 | [Tsukishiro Yanagi](https://discord.com/channels/894925535870865498/1521444394576642118/1528644989725184072) |
| 11 | [Asaba Harumasa](https://discord.com/channels/894925535870865498/1521444394576642118/1528590506370793613) | 44 | [Koleda Belobog](https://discord.com/channels/894925535870865498/1521444394576642118/1528625469677633586) | 77 | [Ukinami Yuzuha](https://discord.com/channels/894925535870865498/1521444394576642118/1528645448821379133) |
| 12 | [Astra Yao](https://discord.com/channels/894925535870865498/1521444394576642118/1528591014137434162) | 45 | [Komano Manato](https://discord.com/channels/894925535870865498/1521444394576642118/1538915503140245554) | 78 | [Ukinami Yuzuha Swimwear](https://discord.com/channels/894925535870865498/1521444394576642118/1533325857156890687) |
| 13 | [Astra Yao Chandelier](https://discord.com/channels/894925535870865498/1521444394576642118/1528591293821882408) | 46 | [Komano Manato White Heart Silhouette](https://discord.com/channels/894925535870865498/1521444394576642118/1528730242665939078) | 79 | [Velina](https://discord.com/channels/894925535870865498/1521444394576642118/1528646007108403232) |
| 14 | [Banyue](https://discord.com/channels/894925535870865498/1521444394576642118/1539494259026038794) | 47 | [Lighter](https://discord.com/channels/894925535870865498/1521444394576642118/1539525310545141810) | 80 | [Velina Shade of Leisure](https://discord.com/channels/894925535870865498/1521444394576642118/1528646232673882163) |
| 15 | [Billy Kid](https://discord.com/channels/894925535870865498/1521444394576642118/1539503466265968700) | 48 | [Lucia Beta](https://discord.com/channels/894925535870865498/1521444394576642118/1528635775057395713) | 81 | [Vivian Banshee](https://discord.com/channels/894925535870865498/1521444394576642118/1528646558902652958) |
| 16 | [Starlight Billy](https://discord.com/channels/894925535870865498/1521444394576642118/1539505781072859186) | 49 | [Lucia](https://discord.com/channels/894925535870865498/1521444394576642118/1528636038489178213) | 82 | [Vivian Banshee Iris of The Shore](https://discord.com/channels/894925535870865498/1521444394576642118/1533323867832057998) |
| 17 | [Belle](https://discord.com/channels/894925535870865498/1521444394576642118/1528591540987891773) | 50 | [Lucy](https://discord.com/channels/894925535870865498/1521444394576642118/1528636779455057950) | 83 | [Von Lycaon](https://discord.com/channels/894925535870865498/1521444394576642118/1528646968232906752) |
| 18 | [Belle Delicate Sunlight](https://discord.com/channels/894925535870865498/1521444394576642118/1540001435603701830) | 51 | [Princess on holiday Lucy](https://discord.com/channels/894925535870865498/1521444394576642118/1528637046996992110) | 84 | [Wise](https://discord.com/channels/894925535870865498/1521444394576642118/1528647179604852836) |
| 19 | [Belle Homewear](https://discord.com/channels/894925535870865498/1521444394576642118/1528592161300283433) | 52 | [Nangong Yu](https://discord.com/channels/894925535870865498/1521444394576642118/1528637358575063120) | 85 | [Wise Homewear](https://discord.com/channels/894925535870865498/1521444394576642118/1528647379161448680) |
| 20 | [Belle Swimwear](https://discord.com/channels/894925535870865498/1521444394576642118/1540004351500619867) | 53 | [Nangong Yu Rhapsody's Muse](https://discord.com/channels/894925535870865498/1521444394576642118/1528637793700417567) | 86 | [Wise Soaring Crane](https://discord.com/channels/894925535870865498/1521444394576642118/1528647591695351819) |
| 21 | [Belle Brilliance of Star](https://discord.com/channels/894925535870865498/1521444394576642118/1539998081766924369) | 54 | [Nekomata](https://discord.com/channels/894925535870865498/1521444394576642118/1528638353526882415) | 87 | [Wise Swimwear](https://discord.com/channels/894925535870865498/1521444394576642118/1528647822818283610) |
| 22 | [Ben Bigger](https://discord.com/channels/894925535870865498/1521444394576642118/1528592957240901743) | 55 | [Nicole Demara](https://discord.com/channels/894925535870865498/1521444394576642118/1528638638265602129) | 88 | [Wise Oath of Skies](https://discord.com/channels/894925535870865498/1521444394576642118/1535919388090171522) |
| 23 | [Burnice](https://discord.com/channels/894925535870865498/1521444394576642118/1534508605561110621) | 56 | [Nicole Demara Cunning Cuties](https://discord.com/channels/894925535870865498/1521444394576642118/1528639225639993456) | 89 | [Ye Shunguang](https://discord.com/channels/894925535870865498/1521444394576642118/1528648269251477645) |
| 24 | [Caesar King](https://discord.com/channels/894925535870865498/1521444394576642118/1528600420103229500) | 57 | [Norma](https://discord.com/channels/894925535870865498/1521444394576642118/1528639788763185183) | 90 | [Ye Shunguang Enlightened](https://discord.com/channels/894925535870865498/1521444394576642118/1528648508318552185) |
| 25 | [Chinatsu Remiel/Sunna](https://discord.com/channels/894925535870865498/1521444394576642118/1528614162714853506) | 58 | [Pan Yinhu](https://discord.com/channels/894925535870865498/1521444394576642118/1528640228133179474) | 91 | [Ye Shunguang Touch of Dawnlight](https://discord.com/channels/894925535870865498/1521444394576642118/1528648776456208404) |
| 26 | [Chinatsu Remiel/Sunna Afternoon Tea Break](https://discord.com/channels/894925535870865498/1521444394576642118/1528614415862337659) | 59 | [Culinary Jewel Pan Yinhu](https://discord.com/channels/894925535870865498/1521444394576642118/1536168703693947011) | 92 | [Ye Shunguang Touch of Dawnlight Enlightened](https://discord.com/channels/894925535870865498/1521444394576642118/1528648993351925834) |
| 27 | [Cissia](https://discord.com/channels/894925535870865498/1521444394576642118/1539513691010109532) | 60 | [Piper Wheel](https://discord.com/channels/894925535870865498/1521444394576642118/1528640797530919014) | 93 | [Yixuan](https://discord.com/channels/894925535870865498/1521444394576642118/1528725249682702427) |
| 28 | [Corrin Wickes](https://discord.com/channels/894925535870865498/1521444394576642118/1539514664474509362) | 61 | [Promeia](https://discord.com/channels/894925535870865498/1521444394576642118/1528641309085270067) | 94 | [Yixuan Trails of Ink](https://discord.com/channels/894925535870865498/1521444394576642118/1528649732971565076) |
| 29 | [Claret](https://discord.com/channels/894925535870865498/1521444394576642118/1531191054072549447) | 62 | [Pulchra](https://discord.com/channels/894925535870865498/1521444394576642118/1534596905307210001) | 95 | [Yidhari](https://discord.com/channels/894925535870865498/1521444394576642118/1529543842599145472) |
| 30 | [New Claret](https://discord.com/channels/894925535870865498/1521444394576642118/1532993374188212356) | 63 | [Pyrois](https://discord.com/channels/894925535870865498/1521444394576642118/1528642203008766123) | 96 | [Zhu Yuan](https://discord.com/channels/894925535870865498/1521444394576642118/1528650517838954587) |
| 31 | [New NEW Claret](https://discord.com/channels/894925535870865498/1521444394576642118/1539191868414500914) | 64 | [Qingyi](https://discord.com/channels/894925535870865498/1521444394576642118/1528642388803981413) | 97 | [Zhao](https://discord.com/channels/894925535870865498/1521444394576642118/1535167966168227880) |
| 32 | [Dialyn](https://discord.com/channels/894925535870865498/1521444394576642118/1528616628860747786) | 65 | [Remielle Dan Light](https://discord.com/channels/894925535870865498/1521444394576642118/1538574557898739873) |  |  |
| 33 | [Ellen Joe](https://discord.com/channels/894925535870865498/1521444394576642118/1537636624211640440) | 66 | [Remielle Dan Dark](https://discord.com/channels/894925535870865498/1521444394576642118/1538565665022283817) |  |  |

## NPC (30)

| # | Model | # | Model | # | Model |
|---|-------|---|-------|---|-------|
| 1 | [Dracaene Sunbringer](https://discord.com/channels/894925535870865498/1521444394576642118/1529265301068316913) | 11 | [Coco](https://discord.com/channels/894925535870865498/1521444394576642118/1531513934450786334) | 21 | [Sarah](https://discord.com/channels/894925535870865498/1521444394576642118/1531558241396326530) |
| 2 | [Lindverine Sunbringer](https://discord.com/channels/894925535870865498/1521444394576642118/1531189529916997796) | 12 | [Crowe](https://discord.com/channels/894925535870865498/1521444394576642118/1531514399309955173) | 22 | [Severian lowell](https://discord.com/channels/894925535870865498/1521444394576642118/1531896927350821016) |
| 3 | [Claret](https://discord.com/channels/894925535870865498/1521444394576642118/1531191054072549447) | 13 | [Effy](https://discord.com/channels/894925535870865498/1521444394576642118/1531515696339746929) | 23 | [Spicy Hotpot Restaurant Owner](https://discord.com/channels/894925535870865498/1521444394576642118/1531559034153472100) |
| 4 | [Silver Squad Replica A](https://discord.com/channels/894925535870865498/1521444394576642118/1531503266733625354) | 14 | [Lin Weiming](https://discord.com/channels/894925535870865498/1521444394576642118/1531552454913560576) | 24 | [Susie](https://discord.com/channels/894925535870865498/1521444394576642118/1531559693603045416) |
| 5 | [Asha](https://discord.com/channels/894925535870865498/1521444394576642118/1531507075513843742) | 15 | [Lucius](https://discord.com/channels/894925535870865498/1521444394576642118/1531553153164775506) | 25 | [Sweety](https://discord.com/channels/894925535870865498/1521444394576642118/1531560360841183342) |
| 6 | [Bertha](https://discord.com/channels/894925535870865498/1521444394576642118/1531510124441768017) | 16 | [Layla](https://discord.com/channels/894925535870865498/1521444394576642118/1531553541293080586) | 26 | [Tarshi](https://discord.com/channels/894925535870865498/1521444394576642118/1531560974954397766) |
| 7 | [Big Daddy](https://discord.com/channels/894925535870865498/1521444394576642118/1531510620120289401) | 17 | [Mors](https://discord.com/channels/894925535870865498/1521444394576642118/1531554543093944330) | 27 | [Twiggy](https://discord.com/channels/894925535870865498/1521444394576642118/1531561305591251014) |
| 8 | [Carinus](https://discord.com/channels/894925535870865498/1521444394576642118/1531512389944737803) | 18 | [Orchidea](https://discord.com/channels/894925535870865498/1521444394576642118/1531556742666653736) | 28 | [Vesper](https://discord.com/channels/894925535870865498/1521444394576642118/1531562236177285120) |
| 9 | [Carole](https://discord.com/channels/894925535870865498/1521444394576642118/1531513070688534638) | 19 | [Charles Perlman](https://discord.com/channels/894925535870865498/1521444394576642118/1531557267269226598) | 29 | [Ray](https://discord.com/channels/894925535870865498/1521444394576642118/1531562758628311070) |
| 10 | [Cecilia](https://discord.com/channels/894925535870865498/1521444394576642118/1531513617885823130) | 20 | [Pompey](https://discord.com/channels/894925535870865498/1521444394576642118/1531557661168898128) | 30 | [Trivia](https://discord.com/channels/894925535870865498/1521444394576642118/1532032072997404832) |

## Special Thanks

- [festivities](https://github.com/festivities) | Shaders
- [Just_ScaasI](https://x.com/Just_ScaasI) | Shaders
- [BonnyAnimations](https://github.com/BonnyAnimations) | Shaders
- Aiko | Shaders
- [Melioli](https://github.com/Melioli) | HoyoToon CDN
- [Poke](https://x.com/Enthralpy) | Rigging
- [Stormz67](https://x.com/stormz67?lang=en) | ZZZ Setup

> [!NOTE]
> You may want to use [DownGit](https://downgit.evecalm.com/#/home) to download individual files that you need instead of cloning the entire repository
