import json
import os
from pathlib import Path

ARTICLES = [
    {
        "id": "solar_system_medium",
        "title": "Our Solar System",
        "author": "Science Team",
        "source": "educational",
        "category": "science",
        "difficulty": "medium",
        "language": "en",
        "tags": ["space", "planets"],
        "text": "The Solar System is made up of the Sun and all the objects that orbit around it. The Sun is a star, and it is the largest object in our solar system. There are eight planets that orbit the Sun. The inner rocky planets are Mercury, Venus, Earth, and Mars. The outer gas giants are Jupiter, Saturn, Uranus, and Neptune. Jupiter is the largest planet, and it has a famous storm called the Great Red Spot. Earth is the only planet we know of that has life, because it has liquid water and the perfect atmosphere."
    },
    {
        "id": "dinosaurs_easy",
        "title": "The Dinosaurs",
        "author": "History Team",
        "source": "educational",
        "category": "history",
        "difficulty": "easy",
        "language": "en",
        "tags": ["animals", "past"],
        "text": "Millions of years ago, dinosaurs lived on Earth. Some dinosaurs were very tall and ate leaves from high trees. Other dinosaurs were fast and hunted for meat. The most famous dinosaur is the T-Rex. It had sharp teeth and short arms. Dinosaurs do not live on Earth anymore. Scientists learn about them by studying old bones called fossils."
    },
    {
        "id": "photosynthesis_hard",
        "title": "How Plants Make Food",
        "author": "Biology Team",
        "source": "educational",
        "category": "science",
        "difficulty": "hard",
        "language": "en",
        "tags": ["plants", "biology"],
        "text": "Photosynthesis is the fascinating biological process by which green plants, algae, and some bacteria convert light energy into chemical energy. During this process, plants capture sunlight using a green pigment called chlorophyll, which is located in their chloroplasts. They absorb carbon dioxide from the air and water from the soil to produce glucose, a type of sugar that provides energy for growth. As a remarkable byproduct of this chemical reaction, plants release oxygen into the atmosphere, which is essential for the survival of most living organisms on Earth."
    },
    {
        "id": "moon_landing_medium",
        "title": "The First Moon Landing",
        "author": "Space History",
        "source": "educational",
        "category": "history",
        "difficulty": "medium",
        "language": "en",
        "tags": ["space", "history"],
        "text": "In July 1969, an American spacecraft called Apollo 11 traveled to the Moon. It was a historic mission because it was the first time humans walked on another world. Astronaut Neil Armstrong was the first person to step onto the lunar surface. As he stepped down, he said his famous words: 'That is one small step for man, one giant leap for mankind.' Buzz Aldrin joined him shortly after. They collected moon rocks and planted an American flag before returning safely to Earth."
    },
    {
        "id": "volcanoes_medium",
        "title": "Inside a Volcano",
        "author": "Earth Science",
        "source": "educational",
        "category": "science",
        "difficulty": "medium",
        "language": "en",
        "tags": ["earth", "geology"],
        "text": "A volcano is an opening in the Earth's crust where hot liquid rock comes out. Deep underground, rocks melt into a thick liquid called magma. When pressure builds up, the magma rises and erupts through the surface. Once the magma reaches the outside air, it is called lava. Some volcanoes erupt violently with huge clouds of ash and gas. Other volcanoes have slow-moving rivers of red-hot lava. Over time, the cooled lava builds up to form tall, cone-shaped mountains."
    }
]

def create_articles():
    base_dir = Path("articles/system")
    for art in ARTICLES:
        lang = art["language"]
        diff = art["difficulty"]
        cat = art["category"]
        
        # Create directory
        dir_path = base_dir / lang / diff / cat
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Save text file
        txt_path = dir_path / f"{art['id']}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(art["text"])
            
        # Save JSON metadata
        json_path = dir_path / f"{art['id']}.json"
        meta = {k:v for k,v in art.items() if k != "text"}
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4)
            
    print("Articles created successfully!")

if __name__ == "__main__":
    create_articles()
