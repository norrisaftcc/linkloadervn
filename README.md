linkloader

License: https://unlicense.org/

demo of renpy scripting using generated assets. 
Sample playthrough (v1.2, 10/31/22) - https://youtu.be/DO8mH-KPFnE
updated 11/2 - https://youtu.be/1PgRyBjnwuk

Demo download: https://terminalcowboy.itch.io/terminalcowboy
----
[The Premise and Game mechanics]

You're a space cowboy, fixing broken link loaders. 
beware of cdr rustlers!

(cons car cdr) -> (car cdr)

(while next_cargo ( load ( cargo next) ) )

[You are a:]

Cosmonaut Cowboy Coder Person (CCCP)
aka (((P)))
*cue patriotic theme*

You have three stats:
- Cosmonaut - your skill with space stuff, high tech, using rayguns
- Cowboy - your skill with desert stuff, low tech, using shotguns
- Coder - your skill with robot stuff, communication, charisma, using terminals
- Person - uh... it's kind of your fourth stat, but you're the only creature on the planet who knows what a "person" is, so it's irrelevant

Robots have a LISP, by the way. It sounds like "(sh)", and it's how you say a parenthesis.

so (((P))) is "sh-sh-sh-p"

or "sh-while next_cargo sh-load sh-cargo next"

If you have low coder, you just say "shucks" a lot and never noticed parentheses.

Quick Character Creation: Pick One of these:

- "Welcome Comrade" COS +2 COW -1 COD +2 -> You're from space, and you're here to help.
- "Howdy Pardner"  COS -1 COW +2 COD +2 -> You ride the range, and you're here to help.
- "Major Tom" COS +2 COW +2 COD -1 -> You were lost in space, and you just crashed here.

(if you want "derived" stats like many RPGs:
- ST = Cos + Cow, DX = Cos + Cow, INT/WIS = Cos + Cod, CHA = Cod
- HP = add up all 3 stats, then add 1 for Person.)


----
Notes on User Stories

Here are some pointers as to how you might write user stories for a game.
First, phrase the  Premise of your game as a question. This is often a yes/no question , but doesn't have to be.
Examples:

    "You're Mario. Can you get to the top of the construction site to rescue Pauline from Donkey Kong?"
    "Can you find the Holy Grail at the bottom of the dungeon before the monsters defeat you?"

Next, make a note of what  Challenge types you want to include (such as combat or puzzles). 
Then write a sentence or two about how  Advancement works. Remember, generally this includes:

    Effectiveness ("I got +1 damage with this new gun")
    Resources ("I brought 99 health potions this time, that boss is NOT going to kill me again")
    Positioning ("This new spell/skill I bought will let me handle this fight differently")

Part Two

Now that you've got a clearer idea about your game concept, it's time to write User Stories
Refresher on User Stories:  https://youtu.be/apOvF9NVguA 

Write three to five user stories about the game, keeping in mind that the user is the player.
- As a [player], I want to be able to [blank] so that I can [blank]
Example:
- "As a space marine, I want to be able to pick up ammunition for my shotgun, so I can keep killing zombies."
- "As a 1940s private eye, I want to be able to find clues, so that I can solve the mystery."

(You can just write these as "As a player" if you want, or you can use the character instead.)

Try to come up with at least three user stories, such as one per Effectiveness, Resources, and Positioning. It's likely that once you have an idea, you'll be able to come up with two each. This should be sufficient for the small scope of this project.
