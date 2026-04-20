# literacy_data.py

class LiteracyStory:
    def __init__(self, story, questions):
        self.story = story
        self.questions = questions

class Grade4Story(LiteracyStory):
    pass

class Grade5Story(LiteracyStory):
    pass

class Grade6Story(LiteracyStory):
    pass

LITERACY_DATABASE = {
   '4': [
        {'story': "The Carabao and the Shell: A carabao mocked a shell for being slow. They raced, but the shell's cousins hid along the path, answering 'I am here' every time the carabao called out. The carabao lost.", 
         'qs': [("Who was mocked for being slow?", "shell"), ("Who helped the shell win?", "cousins"), ("Did the carabao win?", "no")]},
        {'story': "The Legend of the Pineapple: A lazy girl named Pina always said she couldn't find things. Her mother wished she had a thousand eyes. Pina disappeared and a fruit with many 'eyes' grew.", 
         'qs': [("What was the girl's name?", "pina"), ("What did the mother wish for?", "eyes"), ("Was Pina a hard worker?", "no")]},
        {'story': "Si Malakas at Si Maganda: According to legend, a great bird pecked a bamboo cane. The cane split open, and the first man and woman stepped out to inhabit the islands.", 
         'qs': [("What animal pecked the cane?", "bird"), ("What plant did they come from?", "bamboo"), ("How many people stepped out?", "two")]},
        {'story': "The Sun and the Moon: Long ago, the Sun and Moon were married. After a fight, the Moon fled into the night sky, and the Sun has been chasing her ever since.", 
         'qs': [("Were the Sun and Moon married?", "yes"), ("Where did the Moon flee?", "night sky"), ("Is the Sun still chasing her?", "yes")]},
        {'story': "Ants and the Rainy Season: Ants spend all summer gathering crumbs and seeds. When the heavy rains come in June, they stay safe underground with plenty of food.", 
         'qs': [("What do ants gather?", "seeds"), ("In what month do rains start?", "june"), ("Where do they stay safe?", "underground")]},
        {'story': "The Mango Tree: The mango is the national fruit of the Philippines. It is shaped like a heart and turns yellow when it is sweet and ripe.", 
         'qs': [("What is the national fruit?", "mango"), ("What shape is the fruit?", "heart"), ("What color is it when ripe?", "yellow")]},
        {'story': "Cleaning the Yard: Ben and Lea used a broomstick (walis tingting) to gather the fallen leaves. They put the leaves in a compost pit to make fertilizer.", 
         'qs': [("What tool did they use?", "broomstick"), ("What did they gather?", "leaves"), ("Where did they put the leaves?", "compost pit")]},
        {'story': "Diet and Health: Eating local vegetables like malunggay and squash helps children grow strong. These plants are full of vitamins that protect the body.", 
         'qs': [("Name one vegetable mentioned.", ["malunggay", "squash"]), ("What do these plants have?", "vitamins"), ("Do they make you strong?", "yes")]},
        {'story': "The School Garden: Our class planted tomatoes and eggplants. We water them every morning before the sun gets too hot so they don't wither.", 
         'qs': [("What did the class plant?", ["tomatoes", "eggplants", "tomatoes and eggplants", "eggplants and tomatoes"]), ("When do they water them?", "morning"), ("Why water them early?", "sun")]},
        {'story': "Fishermen at Sea: Mang Mario goes out to sea at night. He uses a lamp to attract fish into his net. He returns at dawn with a full boat.", 
         'qs': [("What time does he go out?", "night"), ("What does he use to attract fish?", "lamp"), ("When does he return?", "dawn")]}
    ],
    '5': [
        {'story': "The Rice Terraces: Built 2,000 years ago in Ifugao, these 'Stairs to Heaven' show the engineering skill of ancient Filipinos who used only their hands and stones.", 
         'qs': [("Where are these located?", "ifugao"), ("How many years ago were they built?", "2000"), ("What materials were used?", ["stones", "hands", "hands and stones", "stones and hands"])]},
        {'story': "The Monkey and the Turtle: They split a banana tree. The monkey took the top with leaves, but it died. The turtle took the roots and it grew into a big tree.", 
         'qs': [("What tree did they split?", "banana"), ("Which part did the monkey take?", "top"), ("Whose part grew?", "turtle")]},
        {'story': "Mount Mayon: Known for its perfect cone shape, this volcano in Albay is beautiful but dangerous. It is named after the legendary heroine, Daragang Magayon.", 
         'qs': [("What is its famous shape?", "cone"), ("In what province is it?", "albay"), ("Who is it named after?", "magayon")]},
        {'story': "The Philippine Eagle: This bird is the king of the Philippine skies. It is one of the largest and most powerful eagles in the world but is now critically endangered.", 
         'qs': [("What is the bird's name?", "philippine eagle"), ("Is it powerful?", "yes"), ("Is it endangered?", "yes")]},
        {'story': "Dr. Jose Rizal: Our national hero was a doctor, writer, and artist. He used his novels, Noli Me Tangere and El Filibusterismo, to fight for Philippine freedom.", 
         'qs': [("Who is the national hero?", "jose rizal"), ("What was his profession?", "doctor"), ("How many novels are named?", "two")]},
        {'story': "Typhoon Safety: When a storm signal is raised, families should prepare an emergency kit with flashlights, canned food, and clean water to stay safe.", 
         'qs': [("What should be prepared?", "emergency kit"), ("Name one item in the kit.", ["flashlight", "flashlights", "canned food", "clean water", "water"]), ("Why prepare these?", "safety")]},
        {'story': "The Chocolate Hills: During the dry season, the grass on these 1,200 hills in Bohol turns brown, making them look like giant chocolate drops.", 
         'qs': [("How many hills are there?", "1200"), ("In what province are they?", "bohol"), ("What color is the grass?", "brown")]},
        {'story': "Photosynthesis: Plants are unique because they make their own food. Using sunlight, water, and carbon dioxide, they produce glucose and release oxygen.", 
         'qs': [("What do plants use?", "sunlight"), ("What is the food they make?", "glucose"), ("What gas is released?", "oxygen")]},
        {'story': "The Bahay Kubo: This traditional house is made of bamboo and nipa. It is designed to let air circulate, keeping the family cool during the hot summer months.", 
         'qs': [("What is the house called?", "bahay kubo"), ("What is it made of?", "bamboo"), ("Does it keep families cool?", "yes")]},
        {'story': "Community Pantry: During hard times, people set up carts with free food. The rule is: 'Give what you can, take what you need.' This shows the spirit of Bayanihan.", 
         'qs': [("What is given for free?", "food"), ("What is the rule?", "take what you need"), ("What spirit is shown?", "bayanihan")]}
    ],
    '6': [
        {'story': "Renewable Energy: The Bangui Wind Farm in Ilocos Norte uses 20 massive turbines to convert wind into electricity, providing clean power to thousands of homes.", 
         'qs': [("Where is the wind farm?", "ilocos norte"), ("How many turbines are there?", "20"), ("What is converted to power?", "wind")]},
        {'story': "The Battle of Mactan: In 1521, Lapu-Lapu defended his island against Ferdinand Magellan. This marked the first successful resistance against Spanish colonization.", 
         'qs': [("In what year did this happen?", "1521"), ("Who defended the island?", "lapu-lapu"), ("Who was the explorer?", "magellan")]},
        {'story': "The Water Cycle: Water evaporates from the ocean, condenses into clouds, and falls as rain. This continuous cycle ensures the earth has a steady supply of fresh water.", 
         'qs': [("Where does water evaporate from?", "ocean"), ("What do clouds turn into?", "rain"), ("Is the cycle continuous?", "yes")]},
        {'story': "Digital Citizenship: As students use the internet for research, they must learn to identify 'fake news.' Always check the source before sharing information online.", 
         'qs': [("What is the internet used for?", "research"), ("What should you avoid?", "fake news"), ("What must you check?", "source")]},
        {'story': "Biodiversity: The Philippines is one of the world's 17 megadiverse countries. However, habitat loss due to illegal logging threatens many unique species.", 
         'qs': [("How many megadiverse countries?", "17"), ("What threatens species?", "illegal logging"), ("Is the PH diverse?", "yes")]},
        {'story': "Global Warming: The burning of fossil fuels increases carbon dioxide in the atmosphere. This traps heat, causing glaciers to melt and sea levels to rise.", 
         'qs': [("What gas is increased?", "carbon dioxide"), ("What happens to glaciers?", "melt"), ("What rises?", "sea levels")]},
        {'story': "The Katipunan: Andres Bonifacio founded this secret society to win independence from Spain. Members signed their names in blood to show their loyalty.", 
         'qs': [("Who founded the society?", "andres bonifacio"), ("Who was the enemy?", "spain"), ("What was used to sign names?", "blood")]},
        {'story': "Space Exploration: In 1969, Neil Armstrong became the first human to walk on the moon. He famously called it 'one giant leap for mankind.'", 
         'qs': [("In what year did he walk on moon?", "1969"), ("Who was the first human?", "neil armstrong"), ("What was the leap for?", "mankind")]},
        {'story': "Volcanic Eruptions: When Mount Pinatubo erupted in 1991, it ejected billions of tons of ash. This caused global temperatures to drop for over a year.", 
         'qs': [("What volcano erupted?", "pinatubo"), ("In what year?", "1991"), ("What dropped globally?", "temperatures")]},
        {'story': "The Bill of Rights: The Philippine Constitution includes a Bill of Rights that protects citizens' freedom of speech, religion, and the right to a fair trial.", 
         'qs': [("What document is mentioned?", "constitution"), ("What does it protect?", "freedom"), ("Is speech protected?", "yes")]}
    ]
}
