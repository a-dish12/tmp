def get_recipe_fixtures():
	recipe_fixtures = [
		{
	        'title': 'Avocado Toast with Poached Eggs',
	        'description': 'Creamy avocado on crispy toast, topped with a perfectly poached egg for a nutritious breakfast.',
	        'ingredients': '2 slices of whole grain bread\n1 ripe avocado\n2 large eggs\nSalt and pepper\nOlive oil (optional)\nRed pepper flakes (optional)',
	        'instructions': '1. Toast the bread until golden and crisp.\n2. Mash the avocado in a bowl with salt and pepper (add a drizzle of olive oil if desired).\n3. Bring a small pot of water to a gentle simmer and poach the eggs for 2–3 minutes until whites are set and yolks are soft.\n4. Spread the mashed avocado evenly over the toast.\n5. Top each slice with a poached egg, season with salt, pepper, and red pepper flakes if using.\n6. Serve immediately.',
			'time': 15,
	        'meal_type': 'Breakfast',
			'image_url': 'https://eggcellent.recipes/wp-content/uploads/2024/02/Avocado-Toast-with-Poached-Egg-Recipe-1024x1024.png'
	    },
	    {
	        'title': 'Classic Caesar Salad',
	        'description': 'A crispy romaine lettuce salad with tangy Caesar dressing, croutons, and parmesan cheese.',
	        'ingredients': '4 cups romaine lettuce\n½ cup Caesar dressing\n¼ cup grated parmesan\n½ cup croutons\nFresh ground black pepper',
	        'instructions': '1. Wash and dry the romaine lettuce, then chop into bite-sized pieces.\n2. Place the lettuce in a large bowl.\n3. Add the Caesar dressing and toss until the lettuce is evenly coated.\n4. Sprinkle in the grated parmesan and croutons.\n5. Finish with fresh ground black pepper to taste.\n6. Serve immediately.',
			'time': 10,
	        'meal_type': 'Lunch',
			'image_url': 'https://www.thespruceeats.com/thmb/DRaBINVopeoHOpjJn66Yh7pMBSc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/classic-caesar-salad-recipe-996054-Hero_01-33c94cc8b8e841ee8f2a815816a0af95.jpg'
	    },
		{
	        'title': 'Beef Wellington',
	        'description': 'A rich and flavorful beef fillet wrapped in prosciutto, mushrooms, and puff pastry, baked to perfection.',
	        'ingredients': '1 lb beef tenderloin\n2 cups cremini mushrooms, chopped\n2 tbsp olive oil\n1 tbsp Dijon mustard\n8 oz prosciutto\n1 sheet puff pastry\n1 egg (for egg wash)\nSalt and pepper',
	        'instructions': '1. Preheat the oven to 200°C (400°F).\n2. Season the beef tenderloin with salt and pepper and sear it in olive oil over high heat until browned on all sides. Remove and let cool.\n3. Finely chop the mushrooms and sauté in olive oil until moisture evaporates and mushrooms are golden. Let cool.\n4. Brush the cooled beef with Dijon mustard.\n5. Lay out the prosciutto slices on a sheet of plastic wrap, spread the mushroom mixture on top, and place the beef in the center. Wrap tightly.\n6. Roll out the puff pastry and wrap it around the beef-prosciutto-mushroom bundle, sealing the edges.\n7. Brush the puff pastry with beaten egg.\n8. Bake for 35–45 minutes, or until the pastry is golden and the beef reaches desired doneness.\n9. Let rest for 10 minutes before slicing and serving.',
			'time': 120,
	        'meal_type': 'Dinner',
			'image_url': 'https://www.foodandwine.com/thmb/2k2Kq24_fMvHCyLMPRSNrpg5QdE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/beef-wellington-FT-RECIPE0321-c9a63fccde3b45889ad78fdad078153f.jpg'
	    },
	    {
	        'title': 'Spaghetti Carbonara',
	        'description': 'A creamy, savory pasta with pancetta, eggs, and parmesan cheese. Perfectly comforting.',
	        'ingredients': '200g spaghetti\n100g pancetta\n2 large eggs\n1 cup grated parmesan\nSalt and pepper\n1 tbsp olive oil',
	        'instructions': '1. Bring a large pot of salted water to a boil and cook the spaghetti according to package instructions until al dente.\n2. While the pasta cooks, heat olive oil in a pan over medium heat and cook the pancetta until crispy.\n3. In a bowl, whisk together the eggs and grated parmesan, seasoning with black pepper.\n4. Drain the spaghetti, reserving a small amount of pasta water.\n5. Add the hot spaghetti to the pan with the pancetta and remove from heat.\n6. Quickly stir in the egg and cheese mixture, adding a splash of reserved pasta water if needed to create a creamy sauce.\n7. Season with salt and pepper to taste and serve immediately.',
			'time': 20,
	        'meal_type': 'Dinner',
			'image_url': 'https://images.services.kitchenstories.io/6glN_4JhpVS9aUiBS7JnGsuDULA=/3840x0/filters:quality(80)/images.kitchenstories.io/wagtailOriginalImages/R2568-photo-final-_0.jpg'
	    },
	    {
	        'title': 'Blueberry Muffins',
	        'description': 'Soft, fluffy muffins bursting with fresh blueberries, perfect for breakfast or a snack.',
	        'ingredients': '1 ½ cups all-purpose flour\n¾ cup sugar\n2 tsp baking powder\n1 tsp vanilla extract\n1 cup blueberries\n½ cup milk\n1 egg\n⅓ cup melted butter',
	        'instructions': '1. Preheat the oven to 180°C (350°F) and line a muffin tin with paper liners.\n2. In a bowl, mix together the flour, sugar, and baking powder.\n3. In a separate bowl, whisk the milk, egg, melted butter, and vanilla extract.\n4. Add the wet ingredients to the dry ingredients and gently mix until just combined.\n5. Fold in the blueberries carefully.\n6. Divide the batter evenly among the muffin cups.\n7. Bake for 18–20 minutes, or until a toothpick inserted into the center comes out clean.\n8. Allow to cool slightly before serving.',
			'time': 25,
	        'meal_type': 'Snack',
			'image_url': 'https://bakerbynature.com/wp-content/uploads/2011/05/Blueberry-Muffins-1-of-1.jpg'
	    },
	    {
	        'title': 'Vegan Buddha Bowl',
	        'description': 'A colorful, nutrient-packed bowl with quinoa, roasted veggies, and a tahini dressing.',
	        'ingredients': '1 cup quinoa\n1 cup roasted sweet potatoes\n1 cup roasted broccoli\n½ cup chickpeas\n2 tbsp tahini\nLemon juice\nSalt and pepper',
	        'instructions': '1. Rinse the quinoa and cook it according to package instructions, then fluff with a fork.\n2. While the quinoa cooks, roast the sweet potatoes and broccoli until tender and lightly browned.\n3. Warm the chickpeas if desired.\n4. In a small bowl, whisk together the tahini, lemon juice, salt, and pepper to make the dressing.\n5. Assemble the bowl by placing the quinoa at the base.\n6. Top with roasted sweet potatoes, broccoli, and chickpeas.\n7. Drizzle with the tahini dressing and serve.',
			'time': 40,
	        'meal_type': 'Lunch',
			'image_url': 'https://elavegan.com/wp-content/uploads/2021/05/vegan-buddha-bowl-with-chickpeas-avocado-colorful-veggies-and-green-dressing-on-the-side.jpg'
	    },
	    {
	        'title': 'Pancakes with Maple Syrup',
	        'description': 'Fluffy and golden pancakes served with a drizzle of maple syrup, a classic breakfast treat.',
	        'ingredients': '1 ½ cups all-purpose flour\n1 tbsp sugar\n1 tsp baking powder\n1 tsp vanilla extract\n1 cup milk\n2 eggs\n2 tbsp melted butter\nMaple syrup',
	        'instructions': '1. In a bowl, whisk together the flour, sugar, and baking powder.\n2. In a separate bowl, mix the milk, eggs, melted butter, and vanilla extract.\n3. Add the wet ingredients to the dry ingredients and stir until just combined.\n4. Heat a non-stick pan over medium heat and lightly grease if needed.\n5. Pour small amounts of batter into the pan to form pancakes.\n6. Cook until bubbles form on the surface, then flip and cook until golden.\n7. Serve warm with maple syrup.',
			'time': 20,
	        'meal_type': 'Breakfast',
			'image_url': 'https://www.onceuponachef.com/images/2009/08/pancakes-01-1200x1642.jpg'
	    },
	    {
	        'title': 'Chicken Caesar Wrap',
	        'description': 'Grilled chicken, crispy romaine lettuce, and creamy Caesar dressing wrapped in a flour tortilla.',
	        'ingredients': '1 chicken breast, grilled and sliced\n1 large flour tortilla\n2 cups romaine lettuce\n¼ cup Caesar dressing\n¼ cup grated parmesan',
	        'instructions': '1. Lay the flour tortilla flat on a clean surface.\n2. Spread the Caesar dressing evenly over the tortilla.\n3. Layer the sliced grilled chicken and romaine lettuce on top.\n4. Sprinkle with grated parmesan cheese.\n5. Roll the tortilla tightly to form a wrap.\n6. Slice in half and serve immediately.',
			'time': 15,
	        'meal_type': 'Lunch',
			'image_url': 'https://www.kitchenmomy.com/wp-content/uploads/2025/01/Chicken-Caesar-Wrap-1152x1536.jpg'
	    },
	    {
	        'title': 'Vegetable Stir-Fry with Tofu',
	        'description': 'A quick and healthy stir-fry with tofu and assorted vegetables, served with rice.',
	        'ingredients': '1 block firm tofu, cubed\n1 cup broccoli florets\n1 bell pepper, sliced\n1 carrot, sliced\n2 tbsp soy sauce\n1 tbsp sesame oil\n1 cup cooked rice',
	        'instructions': '1. Grill the chicken breast and slice it into thin strips.\n2. Lay the flour tortilla flat on a clean surface.\n3. Spread the Caesar dressing evenly over the tortilla.\n4. Place the romaine lettuce on top of the dressing.\n5. Add the sliced chicken and sprinkle with grated parmesan.\n6. Roll the tortilla tightly to form a wrap.\n7. Slice in half if desired and serve immediately.',
			'time': 25,
	        'meal_type': 'Dinner',
			'image_url': 'https://sagarecipes.com/wp-content/uploads/2025/04/nextgeneracion_httpss.mj_.runql3WYWpapHg_Vegetable_Stir-Fry_wi_091792f8-9024-4ddd-864f-670b16309654_3.png'
	    },
	    {
	        'title': 'Chocolate Chip Cookies',
	        'description': 'Soft, chewy cookies filled with gooey chocolate chips, the perfect dessert for any occasion.',
	        'ingredients': '1 ½ cups all-purpose flour\n1 tsp baking soda\n½ cup butter, softened\n¾ cup brown sugar\n½ cup granulated sugar\n1 tsp vanilla extract\n1 egg\n1 ½ cups chocolate chips',
	        'instructions': '1. Preheat the oven to 175°C (350°F) and line a baking sheet with parchment paper.\n2. In a bowl, mix together the flour and baking soda.\n3. In a separate bowl, cream the softened butter, brown sugar, and granulated sugar until smooth.\n4. Beat in the egg and vanilla extract.\n5. Gradually add the dry ingredients to the wet ingredients and mix until combined.\n6. Fold in the chocolate chips.\n7. Scoop spoonfuls of dough onto the prepared baking sheet.\n8. Bake for 10–12 minutes, or until edges are lightly golden.\n9. Allow cookies to cool slightly before serving.',
			'time': 30,
	        'meal_type': 'Dessert',
			'image_url': 'https://www.shugarysweets.com/wp-content/uploads/2020/05/chocolate-chip-cookies-recipe.jpg'
	    },
		{
	        'title': 'Homemade Croissants',
	        'description': 'Flaky, buttery croissants made from scratch with layers of dough and butter.',
	        'ingredients': '4 cups all-purpose flour\n1 tbsp sugar\n1 tsp salt\n2 tsp active dry yeast\n1 ¼ cups cold butter\n1 cup milk\n1 egg (for egg wash)',
	        'instructions': '1. In a bowl, combine flour, sugar, salt, and yeast.\n2. Add cold butter cut into small pieces and rub into the flour until it resembles coarse crumbs.\n3. Warm the milk slightly and add to the flour mixture, kneading into a smooth dough.\n4. Chill the dough for 30 minutes.\n5. Roll out the dough into a rectangle, fold into thirds, and chill for 30 minutes. Repeat this rolling and folding process 2–3 times to create layers.\n6. Roll out the dough and cut into triangles.\n7. Roll each triangle from the base to the tip to form croissants.\n8. Place on a baking sheet, brush with beaten egg, and let rise until doubled in size.\n9. Preheat the oven to 200°C (400°F) and bake for 15–20 minutes until golden and flaky.\n10. Serve warm.',
			'time': 240,
	        'meal_type': 'Breakfast',
			'image_url': 'https://www.jocooks.com/wp-content/uploads/2012/02/homemade-croissants-1-7.jpg'
	    },
	    {
	        'title': 'Caprese Salad',
	        'description': 'Fresh mozzarella, tomatoes, and basil drizzled with olive oil and balsamic vinegar.',
	        'ingredients': '2 large tomatoes, sliced\n1 ball fresh mozzarella, sliced\n¼ cup fresh basil leaves\n2 tbsp olive oil\n1 tbsp balsamic vinegar\nSalt and pepper',
	        'instructions': '1. Slice the tomatoes and fresh mozzarella into even pieces.\n2. Arrange the tomato and mozzarella slices on a plate, alternating them.\n3. Tuck fresh basil leaves between the slices.\n4. Drizzle olive oil and balsamic vinegar over the top.\n5. Season with salt and pepper to taste.\n6. Serve immediately.',
			'time': 10,
	        'meal_type': 'Lunch',
			'image_url': 'https://www.lilvienna.com/wp-content/uploads/Recipe-Classic-Italian-Caprese-Salad.jpg'
	    },
	    {
	        'title': 'Shakshuka',
	        'description': 'A Middle Eastern dish of poached eggs in a spicy tomato and bell pepper sauce.',
	        'ingredients': '4 eggs\n2 cups diced tomatoes\n1 onion, chopped\n1 bell pepper, chopped\n2 cloves garlic, minced\n1 tsp cumin\n1 tsp paprika\nSalt and pepper\nOlive oil',
	        'instructions': '1. Heat olive oil in a large skillet over medium heat.\n2. Add the chopped onion and bell pepper and sauté until softened.\n3. Stir in the minced garlic, cumin, and paprika, cooking for another minute.\n4. Add the diced tomatoes and simmer for 10–15 minutes until the sauce thickens.\n5. Make small wells in the sauce and crack the eggs into them.\n6. Cover the skillet and cook until the eggs are set to your liking.\n7. Season with salt and pepper and serve warm.',
			'time': 30,
	        'meal_type': 'Breakfast',
			'image_url': 'https://assets.epicurious.com/photos/54b3fcf4d5e8c3e1070abf4c/master/pass/51220220_shakshuka_1x1.jpg'
	    },
	    {
	        'title': 'Beef Tacos',
	        'description': 'Ground beef seasoned with taco spices, served in soft tortillas with toppings.',
	        'ingredients': '1 lb ground beef\n1 packet taco seasoning\n6 soft taco tortillas\n1 cup shredded lettuce\n1 cup diced tomatoes\n½ cup shredded cheddar cheese\nSour cream',
	        'instructions': '1. In a skillet over medium heat, cook the ground beef until browned, breaking it up with a spoon.\n2. Drain any excess fat and stir in the taco seasoning with a little water according to the packet instructions.\n3. Warm the soft taco tortillas in a pan or microwave.\n4. Assemble the tacos by adding the seasoned beef to each tortilla.\n5. Top with shredded lettuce, diced tomatoes, and shredded cheddar cheese.\n6. Add a dollop of sour cream if desired.\n7. Serve immediately.',
			'time': 25,
	        'meal_type': 'Dinner',
			'image_url': 'https://svetb.com/wp-content/uploads/2025/02/Image_3-45.png'
	    },
	    {
	        'title': 'Vegetable Soup',
	        'description': 'A warm and comforting soup filled with a variety of fresh vegetables.',
	        'ingredients': '2 cups diced potatoes\n2 carrots, chopped\n1 onion, chopped\n2 celery stalks, chopped\n2 cups vegetable broth\n1 cup green beans, chopped\n1 cup diced tomatoes\nSalt and pepper',
	        'instructions': '1. In a large pot, heat a little olive oil over medium heat.\n2. Add the onion, carrots, and celery and sauté until softened.\n3. Stir in the diced potatoes and cook for a few minutes.\n4. Pour in the vegetable broth and bring to a boil.\n5. Reduce heat and add the green beans and diced tomatoes.\n6. Simmer for 20–25 minutes, or until all vegetables are tender.\n7. Season with salt and pepper to taste and serve warm.',
			'time': 40,
	        'meal_type': 'Dinner',
			'image_url': 'https://cdn.loveandlemons.com/wp-content/uploads/2014/10/homemade-vegetable-soup.jpg'
	    },
	    {
	        'title': 'Egg Salad Sandwich',
	        'description': 'Creamy egg salad made with mayonnaise and mustard, served between slices of bread.',
	        'ingredients': '4 boiled eggs, chopped\n2 tbsp mayonnaise\n1 tsp mustard\nSalt and pepper\n2 slices whole grain bread',
	        'instructions': '1. Chop the boiled eggs into small pieces.\n2. In a bowl, mix the eggs with mayonnaise, mustard, salt, and pepper until well combined.\n3. Toast the slices of whole grain bread if desired.\n4. Spread the egg salad evenly onto one slice of bread.\n5. Top with the other slice of bread to form a sandwich.\n6. Slice in half if desired and serve immediately.',
			'time': 15,
	        'meal_type': 'Lunch',
			'image_url': 'https://www.spendwithpennies.com/wp-content/uploads/2023/03/1200-Best-Egg-Salad-Recipe-SpendWithPennies.jpg'
	    },
	    {
	        'title': 'Grilled Cheese Sandwich',
	        'description': 'A classic grilled cheese sandwich with gooey melted cheese and crispy golden bread.',
	        'ingredients': '2 slices of bread\n2 slices of cheddar cheese\nButter',
	        'instructions': '1. Butter one side of each slice of bread.\n2. Place one slice of bread, buttered side down, in a heated skillet over medium heat.\n3. Add the cheddar cheese slices on top.\n4. Cover with the second slice of bread, buttered side up.\n5. Cook until the bottom is golden brown, then flip and cook the other side until the cheese is melted and the bread is golden.\n6. Remove from the skillet, slice if desired, and serve immediately.',
			'time': 10,
	        'meal_type': 'Snack',
			'image_url': 'https://static01.nyt.com/images/2021/08/30/dining/as-grilled-cheese-sandwich-on-the-grill/as-grilled-cheese-sandwich-on-the-grill-threeByTwoMediumAt2X.jpg'
	    },
	    {
			"title": "Japanese Onigiri (Rice Balls)",
			"description": "Traditional Japanese rice balls filled with savory ingredients and wrapped in nori.",
			"ingredients": "Short-grain rice\nWater\nSalt\nNori sheets\nTuna fish\nMayonnaise",
			"instructions": "1. Cook the rice according to package instructions and let it cool slightly.\n2. Mix tuna with mayonnaise in a small bowl.\n3. Wet your hands lightly and sprinkle with salt.\n4. Place rice in your palm, add a small amount of tuna filling, and shape gently into a triangle.\n5. Wrap with a strip of nori.\n6. Repeat with remaining rice and filling.\n7. Serve at room temperature.",
			"time": 25,
			"meal_type": "lunch",
			"image_url": "https://www.justonecookbook.com/wp-content/uploads/2023/09/Onigiri-Japanese-Rice-Balls-2071-I-2.jpg"
		},
	    {
	        'title': 'Pesto Pasta',
	        'description': 'Pasta tossed in a flavorful pesto sauce made from basil, garlic, pine nuts, and parmesan.',
	        'ingredients': '200g pasta\n¼ cup pesto sauce\n2 tbsp pine nuts, toasted\nParmesan cheese, grated',
	        'instructions': '1. Bring a large pot of salted water to a boil and cook the pasta according to package instructions until al dente.\n2. Drain the pasta, reserving a small amount of the cooking water.\n3. Return the pasta to the pot and toss with the pesto sauce, adding a splash of reserved water if needed to loosen the sauce.\n4. Sprinkle toasted pine nuts over the pasta.\n5. Serve with grated Parmesan cheese on top.',
			'time': 20,
	        'meal_type': 'Dinner',
			'image_url': 'https://insanelygoodrecipes.com/wp-content/uploads/2022/12/Pesto-Pasta-on-a-Bowl.jpg'
	    },
	    {
	        'title': 'Smoothie Bowl',
	        'description': 'A thick, creamy smoothie topped with fresh fruit, granola, and seeds for extra crunch.',
	        'ingredients': '1 frozen banana\n½ cup frozen mixed berries\n½ cup almond milk\n¼ cup granola\nFresh fruit for topping (e.g., banana, strawberries)',
	        'instructions': '1. In a blender, combine the frozen banana, frozen mixed berries, and almond milk.\n2. Blend until smooth and thick.\n3. Pour the smoothie into a bowl.\n4. Top with granola and fresh fruit slices.\n5. Serve immediately.',
			'time': 10,
	        'meal_type': 'Breakfast',
			'image_url': 'https://healthyfitnessmeals.com/wp-content/uploads/2019/04/instagram-In-Stream_Square___berry-smoothie-bowl-6.jpg'
	    },
	    {
	        'title': 'Chicken Fried Rice',
	        'description': 'Stir-fried rice with chicken, vegetables, and soy sauce, an easy and delicious dinner option.',
	        'ingredients': '1 chicken breast, diced\n2 cups cooked rice\n1 cup frozen peas and carrots\n2 eggs, scrambled\n2 tbsp soy sauce\n1 tbsp sesame oil',
	        'instructions': '1. Heat sesame oil in a large skillet or wok over medium-high heat.\n2. Add the diced chicken and cook until fully cooked.\n3. Push the chicken to one side and scramble the eggs in the same skillet.\n4. Add the cooked rice and frozen peas and carrots, stirring to combine.\n5. Pour in the soy sauce and stir-fry everything together until heated through.\n6. Serve immediately.',
			'time': 30,
	        'meal_type': 'Dinner',
			'image_url': 'https://www.recipetineats.com/tachyon/2019/09/Chicken-fried-rice-copy.jpg'
	    },
	    {
	        'title': 'Apple Cinnamon Oatmeal',
	        'description': 'A warm bowl of oatmeal topped with sautéed apples and cinnamon for a cozy breakfast.',
	        'ingredients': '1 cup rolled oats\n1 apple, diced\n1 tsp cinnamon\n1 tbsp honey\n1 cup milk',
	        'instructions': '1. In a small pot, bring the milk to a gentle boil.\n2. Add the rolled oats and cook over medium heat, stirring occasionally, until thickened.\n3. In a separate pan, sauté the diced apple with cinnamon until tender.\n4. Pour the cooked oats into a bowl.\n5. Top with the sautéed apples and drizzle with honey.\n6. Serve warm.',
			'time': 15,
	        'meal_type': 'Breakfast',
			'image_url': 'https://cozymomjournal.com/wp-content/uploads/2024/08/Apple-Cinnamon-Oatmeal-Recipe-4-735x1103.jpg'
	    },
	    {
	        'title': 'Buffalo Cauliflower Bites',
	        'description': 'Crispy roasted cauliflower coated in spicy buffalo sauce, a great vegetarian snack.',
	        'ingredients': '1 cauliflower head, cut into florets\n½ cup flour\n1 tsp garlic powder\n1 tsp paprika\n1 tsp onion powder\n½ cup buffalo sauce\nOlive oil',
	        'instructions': '1. Preheat the oven to 200°C (400°F) and line a baking sheet with parchment paper.\n2. In a bowl, mix the flour, garlic powder, paprika, and onion powder.\n3. Toss the cauliflower florets in the flour mixture until evenly coated.\n4. Drizzle with a little olive oil and spread the florets on the baking sheet.\n5. Roast for 20 minutes, turning halfway through.\n6. Remove from the oven and toss the roasted cauliflower in buffalo sauce.\n7. Return to the oven for an additional 5 minutes.\n8. Serve immediately.',
			'time': 30,
	        'meal_type': 'Snack',
			'image_url': 'https://gethealthyu.com/wp-content/uploads/2024/09/Buffalo-Cauliflower-Bites-9.jpg'
	    },
		{
	        'title': 'Homemade Lasagna',
	        'description': 'Layers of pasta, rich tomato sauce, creamy ricotta, and melted mozzarella cheese, baked until bubbly.',
	        'ingredients': '12 lasagna noodles\n2 cups ricotta cheese\n1 lb ground beef\n1 jar marinara sauce\n1 onion, chopped\n1 tbsp garlic, minced\n2 cups mozzarella cheese\nParmesan cheese\n2 tbsp olive oil',
	        'instructions': '1. Preheat the oven to 180°C (350°F).\n2. Cook the lasagna noodles according to package instructions, then drain and set aside.\n3. In a skillet, heat olive oil over medium heat and sauté the chopped onion and garlic until fragrant.\n4. Add the ground beef and cook until browned. Stir in the marinara sauce and simmer for 5–10 minutes.\n5. In a baking dish, spread a thin layer of the meat sauce on the bottom.\n6. Layer noodles, ricotta cheese, meat sauce, and mozzarella cheese. Repeat until all ingredients are used, finishing with mozzarella and a sprinkle of Parmesan on top.\n7. Cover with foil and bake for 30–40 minutes.\n8. Remove the foil and bake an additional 10–15 minutes until cheese is bubbly and golden.\n9. Let stand for 10 minutes before serving.',
			'time': 150,
	        'meal_type': 'Dinner',
			'image_url': 'https://topteenrecipes.com/wp-content/uploads/2023/02/Easy-Homemade-Lasagna-Recipe5-683x1024.jpg'
	    },
	    {
	        'title': 'Chicken Shawarma',
	        'description': 'Tender chicken seasoned with shawarma spices, served in pita with garlic sauce and veggies.',
	        'ingredients': '2 chicken breasts, sliced\n1 tbsp shawarma seasoning\n1 tbsp olive oil\n2 pita breads\nGarlic sauce\nLettuce, tomatoes, cucumbers',
	        'instructions': '1. Toss the sliced chicken breasts with shawarma seasoning and olive oil.\n2. Heat a skillet over medium heat and cook the chicken until fully cooked and lightly browned.\n3. Warm the pita breads in a pan or oven.\n4. Spread garlic sauce inside each pita.\n5. Fill the pita with cooked chicken and top with lettuce, tomatoes, and cucumbers.\n6. Serve immediately.',
			'time': 30,
	        'meal_type': 'Dinner',
			'image_url': 'https://www.licious.in/blog/wp-content/uploads/2020/12/Chicken-Shawarma.jpg'
	    },
	    {
	        'title': 'Mango Sticky Rice',
	        'description': 'A sweet Thai dessert made with sticky rice, fresh mango, and a drizzle of coconut milk.',
	        'ingredients': '1 cup sticky rice\n1 ripe mango, sliced\n½ cup coconut milk\n2 tbsp sugar',
	        'instructions': '1. Rinse the sticky rice until the water runs clear.\n2. Cook the sticky rice according to package instructions or by steaming.\n3. In a small saucepan, heat the coconut milk with sugar until the sugar dissolves.\n4. Pour a portion of the sweetened coconut milk over the cooked sticky rice and let it absorb for a few minutes.\n5. Serve the sticky rice with sliced mango on the side.\n6. Drizzle with the remaining coconut milk and serve immediately.',
			'time': 30,
	        'meal_type': 'Dessert',
			'image_url': 'https://www.mob.co.uk/cdn-cgi/image/width=3840,quality=75,format=auto/https://files.mob-cdn.co.uk/recipes/2024/08/Mango-Sticky-Rice.jpg'
	    },
	    {
	        'title': 'Slow Cooker Beef Stew',
	        'description': 'Tender beef chunks, carrots, potatoes, and onions slow-cooked in a savory broth for a hearty meal.',
	        'ingredients': '2 lbs beef chuck, cut into cubes\n4 cups beef broth\n3 carrots, sliced\n3 potatoes, diced\n1 onion, chopped\n2 cloves garlic, minced\n1 tbsp thyme\n2 tbsp flour\nSalt and pepper',
	        'instructions': '1. In a large bowl, toss the beef cubes with flour, salt, and pepper.\n2. In a skillet, sear the beef over medium-high heat until browned on all sides.\n3. Transfer the beef to a slow cooker.\n4. Add the sliced carrots, diced potatoes, chopped onion, minced garlic, thyme, and beef broth.\n5. Stir to combine, cover, and cook on low for 6–8 hours or on high for 3–4 hours, until the beef and vegetables are tender.\n6. Taste and adjust seasoning with salt and pepper.\n7. Serve hot.',
			'time': 180,
	        'meal_type': 'Dinner',
			'image_url': 'https://natashaskitchen.com/wp-content/uploads/2022/11/beef-stew-sq.jpg'
	    },
	    {
	        'title': 'Chicken Parmesan',
	        'description': 'Breaded chicken breasts topped with marinara sauce and melted mozzarella cheese, served with spaghetti.',
	        'ingredients': '4 chicken breasts\n1 cup breadcrumbs\n1 cup flour\n2 eggs\n1 cup marinara sauce\n1 cup mozzarella cheese, shredded\n1 cup parmesan cheese, grated\n1 tbsp olive oil\nSpaghetti',
	        'instructions': '1. Preheat the oven to 200°C (400°F).\n2. Pound the chicken breasts to even thickness.\n3. Set up a breading station: one plate with flour, one bowl with beaten eggs, and one plate with breadcrumbs.\n4. Dredge each chicken breast in flour, dip in egg, then coat with breadcrumbs.\n5. Heat olive oil in a skillet over medium heat and cook the chicken until golden brown on both sides.\n6. Place the chicken in a baking dish, top with marinara sauce, shredded mozzarella, and grated parmesan.\n7. Bake for 20–25 minutes until the cheese is melted and bubbly.\n8. Meanwhile, cook spaghetti according to package instructions.\n9. Serve the chicken parmesan over the cooked spaghetti.',
			'time': 90,
	        'meal_type': 'Dinner',
			'image_url': 'https://hips.hearstapps.com/hmg-prod/images/chicken-parmesan-secondary-644041992a1d4.jpg?crop=1xw:1xh;center,top&resize=980:*'
	    },
	    {
	        'title': 'Pulled Pork Sandwiches',
	        'description': 'Tender, slow-cooked pulled pork served with barbecue sauce and coleslaw on a soft bun.',
	        'ingredients': '3 lbs pork shoulder\n1 onion, sliced\n1 cup barbecue sauce\n2 tbsp brown sugar\n1 tbsp paprika\n1 tbsp garlic powder\n2 cups coleslaw mix\n4 buns',
	        'instructions': '1. Rub the pork shoulder with brown sugar, paprika, garlic powder, salt, and pepper.\n2. Place the sliced onion in the bottom of a slow cooker and put the pork on top.\n3. Pour half of the barbecue sauce over the pork.\n4. Cover and cook on low for 8 hours or until the pork is tender and easily shredded.\n5. Remove the pork and shred it with two forks.\n6. Return the shredded pork to the slow cooker and mix with the remaining barbecue sauce.\n7. Toast the buns if desired.\n8. Assemble sandwiches with pulled pork and top with coleslaw.\n9. Serve immediately.',
			'time': 180,
	        'meal_type': 'Dinner',
			'image_url': 'https://amandascookin.com/wp-content/uploads/2024/02/Pulled-Pork-Sandwiches-V01.jpg'
	    },
	    {
	        'title': 'Beef Bourguignon',
	        'description': 'A French classic: tender beef braised in red wine with onions, mushrooms, and carrots, served over mashed potatoes.',
	        'ingredients': '2 lbs beef chuck, cut into cubes\n1 bottle red wine\n2 cups beef broth\n1 onion, chopped\n2 carrots, sliced\n2 cloves garlic, minced\n2 cups mushrooms, sliced\n2 tbsp flour\nSalt and pepper',
	        'instructions': '1. Preheat the oven to 325°F (160°C).\n2. Toss the beef cubes with flour, salt, and pepper.\n3. In a large oven-safe pot, sear the beef over medium-high heat until browned on all sides. Remove and set aside.\n4. In the same pot, sauté the chopped onion, sliced carrots, and minced garlic until softened.\n5. Add the mushrooms and cook for a few minutes.\n6. Return the beef to the pot and pour in the red wine and beef broth.\n7. Bring to a simmer, cover, and transfer to the oven.\n8. Bake for 2–2.5 hours until the beef is tender.\n9. Serve hot over mashed potatoes.',
			'time': 150,
	        'meal_type': 'Dinner',
			'image_url': 'http://d2k9njawademcf.cloudfront.net/indeximages/3888/original/Beef_Bourguignon.jpg?1380054403'
	    },
	    {
	        'title': 'Paella',
	        'description': 'A traditional Spanish dish made with saffron rice, seafood, chicken, and vegetables, cooked in one pan.',
	        'ingredients': '2 cups Arborio rice\n1 lb chicken thighs, diced\n1 lb shrimp, peeled\n1 cup peas\n1 red bell pepper, chopped\n2 tomatoes, chopped\n1 onion, chopped\n2 cloves garlic, minced\n1 tsp saffron threads\n4 cups chicken broth\nOlive oil',
	        'instructions': '1. Heat olive oil in a large paella pan or wide skillet over medium heat.\n2. Add the diced chicken and cook until browned.\n3. Sauté the chopped onion, garlic, and red bell pepper until softened.\n4. Stir in the chopped tomatoes and cook for a few minutes.\n5. Add the rice and saffron threads, stirring to coat the rice.\n6. Pour in the chicken broth and bring to a simmer.\n7. Add the peas and shrimp, distributing them evenly.\n8. Cook without stirring for 20–25 minutes, until the rice is tender and liquid is absorbed.\n9. Let rest for a few minutes before serving.',
			'time': 120,
	        'meal_type': 'Dinner',
			'image_url': 'https://leckereideen.com/wp-content/uploads/2023/02/Paella-Rezept-mit-Frutti-di-Mare2.jpg'
	    },
	    {
	        'title': 'Braised Short Ribs',
	        'description': 'Tender, fall-off-the-bone short ribs braised in red wine and aromatics, served with mashed potatoes.',
	        'ingredients': '4 beef short ribs\n1 bottle red wine\n2 cups beef broth\n2 onions, chopped\n2 carrots, chopped\n2 cloves garlic, minced\n1 tbsp thyme\nSalt and pepper\nOlive oil',
	        'instructions': '1. Preheat the oven to 325°F (160°C).\n2. Season the short ribs with salt and pepper.\n3. Heat olive oil in a large oven-safe pot and sear the short ribs on all sides until browned. Remove and set aside.\n4. In the same pot, sauté the chopped onions, carrots, and minced garlic until softened.\n5. Add the thyme, red wine, and beef broth, scraping up any browned bits from the bottom.\n6. Return the short ribs to the pot, ensuring they are mostly submerged in the liquid.\n7. Cover and braise in the oven for 2.5–3 hours until the meat is tender and falling off the bone.\n8. Serve hot, ideally over mashed potatoes.',
			'time': 180,
	        'meal_type': 'Dinner',
			'image_url': 'https://s23209.pcdn.co/wp-content/uploads/2022/10/220628_DD_Braised-Short-Ribs_108.jpg'
	    },
	    {
	        'title': 'Roast Duck with Orange Glaze',
	        'description': 'A perfectly roasted duck with a sweet and tangy orange glaze, served with roasted vegetables.',
	        'ingredients': '1 whole duck\n2 oranges, juiced and zested\n1 tbsp honey\n2 tbsp soy sauce\n2 tbsp olive oil\n1 tbsp ginger, minced\n1 tbsp garlic, minced\nSalt and pepper\nRoasted vegetables (e.g., carrots, potatoes)',
	        'instructions': '1. Preheat the oven to 375°F (190°C).\n2. Pat the duck dry and season with salt and pepper.\n3. In a small bowl, mix orange juice and zest, honey, soy sauce, olive oil, minced ginger, and garlic to make the glaze.\n4. Place the duck on a roasting rack in a roasting pan.\n5. Brush the duck with some of the orange glaze.\n6. Roast for 90–120 minutes, basting occasionally with the glaze, until the duck is cooked through and skin is crispy.\n7. Roast your vegetables in the oven alongside the duck during the last 30–40 minutes.\n8. Remove the duck from the oven, let it rest for 10 minutes, then carve and serve with roasted vegetables and remaining glaze.',
			'time': 150,
	        'meal_type': 'Dinner',
			'image_url': 'https://imagedelivery.net/0Mq3wNnVcEg-6tUqy1Ku0g/cg/media/users/104/article_images/Savory%20Roasted%20Duck%20with%20Orange%20Glaze_20250828_215016_7337_20250828_215019_2qfa.jpg/public'
	    },
	    {
	        'title': 'Chicken and Mushroom Risotto',
	        'description': 'A creamy and comforting risotto with tender chicken and earthy mushrooms, perfect for a cozy dinner.',
	        'ingredients': '1 lb chicken breast, diced\n1 cup Arborio rice\n1 cup sliced mushrooms\n1 onion, chopped\n2 cloves garlic, minced\n4 cups chicken broth\n1/2 cup dry white wine\n1/2 cup grated parmesan\nOlive oil\nSalt and pepper',
	        'instructions': '1. Heat olive oil in a large skillet over medium heat and cook the diced chicken until browned and cooked through. Remove and set aside.\n2. In the same skillet, sauté the chopped onion and minced garlic until translucent.\n3. Add the sliced mushrooms and cook until tender.\n4. Stir in the Arborio rice and cook for 1–2 minutes until lightly toasted.\n5. Pour in the white wine and cook until mostly absorbed.\n6. Gradually add the chicken broth, one ladle at a time, stirring constantly and allowing the liquid to be absorbed before adding more.\n7. Continue until the rice is creamy and cooked through, about 20–25 minutes.\n8. Stir the cooked chicken back into the risotto.\n9. Remove from heat and mix in grated Parmesan, adjusting seasoning with salt and pepper.\n10. Serve immediately.',
			'time': 60,
	        'meal_type': 'Dinner',
			'image_url': 'https://www.recipetineats.com/tachyon/2016/08/Chicken-Mushroom-Risotto_6-680x952.jpg'
	    },
	    {
	        'title': 'Stuffed Bell Peppers',
	        'description': 'Colorful bell peppers stuffed with a savory mixture of ground beef, rice, tomatoes, and spices.',
	        'ingredients': '4 bell peppers, tops cut off and seeds removed\n1 lb ground beef\n1 cup cooked rice\n1 can diced tomatoes\n1 onion, chopped\n2 cloves garlic, minced\n1 tsp cumin\n1 tsp paprika\n1 cup shredded mozzarella cheese\nSalt and pepper',
	        'instructions': '1. Preheat the oven to 375°F (190°C).\n2. In a skillet, sauté the chopped onion and minced garlic until softened.\n3. Add the ground beef and cook until browned. Drain excess fat if needed.\n4. Stir in the cooked rice, diced tomatoes, cumin, paprika, salt, and pepper. Cook for a few minutes until well combined.\n5. Stuff each bell pepper with the beef and rice mixture.\n6. Place the stuffed peppers in a baking dish and cover with foil.\n7. Bake for 35–40 minutes.\n8. Remove the foil, sprinkle shredded mozzarella on top, and bake for an additional 10–15 minutes until the cheese is melted and bubbly.\n9. Serve hot.',
			'time': 75,
	        'meal_type': 'Dinner',
			'image_url': 'https://bellyfull.net/wp-content/uploads/2021/01/Stuffed-Peppers-blog-2.jpg'
	    },
	    {
	        'title': 'Chicken Fajitas',
	        'description': 'Sautéed chicken strips with bell peppers and onions, served with tortillas and your favorite toppings.',
	        'ingredients': '2 chicken breasts, sliced\n2 bell peppers, sliced\n1 onion, sliced\n2 tbsp fajita seasoning\n1 tbsp olive oil\n4 flour tortillas\nSour cream, guacamole, and salsa (optional)',
	        'instructions': '1. Heat olive oil in a large skillet over medium-high heat.\n2. Add the sliced chicken and cook until browned and cooked through.\n3. Add the sliced bell peppers and onion, sprinkling the fajita seasoning over the mixture.\n4. Sauté until the vegetables are tender-crisp.\n5. Warm the flour tortillas in a pan or microwave.\n6. Serve the chicken and vegetables on the tortillas with optional sour cream, guacamole, and salsa.',
			'time': 45,
	        'meal_type': 'Dinner',
			'image_url': 'https://i0.wp.com/kristineskitchenblog.com/wp-content/uploads/2023/05/chicken-fajitas-recipe-36-2.jpg?w=1400&ssl=1'
	    },
	    {
	        'title': 'Vegetable Lasagna',
	        'description': 'A hearty vegetarian lasagna made with layers of fresh vegetables, ricotta, and mozzarella cheese.',
	        'ingredients': '12 lasagna noodles\n2 cups ricotta cheese\n2 cups shredded mozzarella\n1 zucchini, sliced\n1 cup spinach\n1 cup sliced mushrooms\n1 jar marinara sauce\n1 onion, chopped\n1 tbsp olive oil\n1 tsp Italian seasoning',
	        'instructions': '1. Preheat the oven to 180°C (350°F).\n2. Cook the lasagna noodles according to package instructions, then drain and set aside.\n3. In a skillet, heat olive oil over medium heat and sauté the chopped onion until softened.\n4. Add the zucchini, mushrooms, spinach, and Italian seasoning, cooking until vegetables are tender.\n5. In a baking dish, spread a layer of marinara sauce.\n6. Layer noodles, ricotta cheese, sautéed vegetables, marinara sauce, and shredded mozzarella. Repeat until all ingredients are used, finishing with mozzarella on top.\n7. Cover with foil and bake for 30–40 minutes.\n8. Remove the foil and bake an additional 10–15 minutes until cheese is melted and bubbly.\n9. Let stand for 10 minutes before serving.',
			'time': 90,
	        'meal_type': 'Dinner',
			'image_url': 'https://cdn.loveandlemons.com/wp-content/uploads/2023/12/vegetarian-lasagna-scaled.jpg'
	    },
	    {
	        'title': 'Grilled Lemon Herb Chicken',
	        'description': 'Tender grilled chicken marinated in lemon, garlic, and herbs, served with roasted vegetables.',
	        'ingredients': '4 chicken breasts\n1 lemon, juiced and zested\n3 cloves garlic, minced\n2 tbsp olive oil\n1 tsp dried oregano\n1 tsp dried thyme\nSalt and pepper\nRoasted vegetables (e.g., carrots, potatoes)',
	        'instructions': '1. In a bowl, combine lemon juice and zest, minced garlic, olive oil, oregano, thyme, salt, and pepper to make a marinade.\n2. Add the chicken breasts to the marinade and let sit for at least 30 minutes.\n3. Preheat the grill to medium-high heat.\n4. Grill the chicken for 6–8 minutes per side, or until fully cooked and juices run clear.\n5. Meanwhile, roast the vegetables in the oven until tender.\n6. Serve the grilled chicken alongside the roasted vegetables.',
			'time': 60,
	        'meal_type': 'Dinner',
			'image_url': 'https://mytastefulrecipes.com/wp-content/uploads/2025/08/Grilled_Lemon_Herb_Chicken_vxcaly.webp'
	    },
	    {
	        'title': 'Peanut Butter Energy Balls',
	        'description': 'No-bake energy balls made with peanut butter, oats, and honey, perfect for a quick snack.',
	        'ingredients': '1 cup rolled oats\n½ cup peanut butter\n¼ cup honey\n1 tbsp chia seeds\n1 tsp vanilla extract\n1 tbsp mini chocolate chips (optional)',
	        'instructions': '1. In a bowl, combine rolled oats, peanut butter, honey, chia seeds, and vanilla extract.\n2. Mix until all ingredients are well incorporated.\n3. If desired, fold in mini chocolate chips.\n4. Roll the mixture into small bite-sized balls.\n5. Place the energy balls on a plate or tray and refrigerate for at least 10 minutes to firm up.\n6. Serve chilled or store in an airtight container.',
			'time': 15,
	        'meal_type': 'Snack',
			'image_url': 'https://gimmedelicious.com/wp-content/uploads/2024/03/easypeanutbutterenergybites-12-1.jpg'
	    },
	    {
			"title": "Black Garlic Mushroom Risotto",
			"description": "Creamy risotto elevated with the deep umami flavor of black garlic.",
			"ingredients": "Arborio rice\nVegetable broth\nBlack garlic\nMushrooms\nOnion\nOlive oil\nParmesan cheese",
			"instructions": "1. Heat olive oil in a pan and sauté chopped onion until soft.\n2. Add sliced mushrooms and cook until browned.\n3. Stir in arborio rice and toast lightly.\n4. Gradually add warm vegetable broth, stirring constantly.\n5. Mash black garlic and mix it into the risotto.\n6. Finish with grated Parmesan and serve hot.",
			"time": 40,
			"meal_type": "dinner",
			"image_url": "https://dishnthekitchen.com/wp-content/uploads/2014/11/BlackGarlicRisotto2.jpg"
		},
	    {
	        'title': 'Chocolate Avocado Mousse',
	        'description': 'A creamy, rich chocolate mousse made with ripe avocado for a healthier dessert.',
	        'ingredients': '2 ripe avocados\n¼ cup cocoa powder\n2 tbsp maple syrup\n1 tsp vanilla extract\nPinch of salt',
	        'instructions': '1. Cut the avocados in half, remove the pits, and scoop the flesh into a blender or food processor.\n2. Add cocoa powder, maple syrup, vanilla extract, and a pinch of salt.\n3. Blend until smooth and creamy.\n4. Taste and adjust sweetness if desired.\n5. Spoon the mousse into serving dishes.\n6. Chill in the refrigerator for at least 10 minutes before serving.',
			'time': 15,
	        'meal_type': 'Dessert',
			'image_url': 'https://betterhomebase.com/wp-content/uploads/2024/10/Chocolate-Avocado-Mousse.webp'
	    },
	    {
	        'title': 'Vegetarian Tacos',
	        'description': 'Soft corn tortillas filled with seasoned black beans, avocado, lettuce, and salsa.',
	        'ingredients': '1 can black beans, drained and rinsed\n4 corn tortillas\n1 avocado, sliced\n1 cup lettuce, shredded\n1 tomato, diced\n1 tbsp taco seasoning\nSalsa',
	        'instructions': '1. In a skillet over medium heat, cook the black beans with taco seasoning until heated through.\n2. Warm the corn tortillas in a pan or microwave.\n3. Fill each tortilla with the seasoned black beans.\n4. Top with sliced avocado, shredded lettuce, diced tomato, and salsa.\n5. Serve immediately.',
			'time': 30,
	        'meal_type': 'Lunch',
			'image_url': 'https://www.twopeasandtheirpod.com/wp-content/uploads/2021/06/Veggie-Tacos4577.jpg'
	    },
	    {
	        'title': 'Cinnamon Roll Pancakes',
	        'description': 'Fluffy pancakes with a cinnamon swirl, topped with icing for a decadent breakfast.',
	        'ingredients': '1 ½ cups pancake mix\n1 tsp cinnamon\n1 egg\n1 cup milk\n2 tbsp butter, melted\nFor the swirl: ¼ cup brown sugar, 1 tsp cinnamon\nFor the icing: ½ cup powdered sugar, 1 tbsp milk',
	        'instructions': '1. In a bowl, combine pancake mix, 1 tsp cinnamon, egg, milk, and melted butter. Stir until smooth.\n2. In a small bowl, mix brown sugar and 1 tsp cinnamon for the swirl.\n3. Heat a non-stick skillet or griddle over medium heat and pour pancake batter onto it.\n4. Sprinkle a little of the cinnamon-sugar mixture onto each pancake and swirl with a toothpick.\n5. Cook until bubbles form on the surface, then flip and cook until golden brown.\n6. For the icing, mix powdered sugar and milk until smooth.\n7. Drizzle the icing over the pancakes before serving.',
			'time': 40,
	        'meal_type': 'Breakfast',
			'image_url': 'https://i.pinimg.com/originals/7a/1d/16/7a1d165e5e06aea70b664edceeeafe60.jpg'
	    },
	    {
	        'title': 'Baked Apple Chips',
	        'description': 'Thinly sliced apples baked until crispy and lightly dusted with cinnamon, a healthy snack.',
	        'ingredients': '4 apples, thinly sliced\n1 tsp cinnamon\n1 tbsp sugar (optional)',
	        'instructions': '1. Preheat the oven to 200°F (95°C) and line a baking sheet with parchment paper.\n2. Arrange the thinly sliced apples in a single layer on the baking sheet.\n3. Sprinkle with cinnamon and sugar if using.\n4. Bake for 40–45 minutes, flipping the slices halfway through, until the apples are crisp.\n5. Let cool completely before serving.',
			'time': 45,
	        'meal_type': 'Snack',
			'image_url': 'https://www.cookingclassy.com/wp-content/uploads/2021/09/baked-apple-chips-2-1024x1536.jpg'
	    },
	    {
	        'title': 'Homemade Granola',
	        'description': 'Crunchy, sweet granola made with oats, honey, and nuts, perfect for breakfast or as a topping for yogurt.',
	        'ingredients': '3 cups rolled oats\n½ cup honey\n1 cup mixed nuts, chopped\n1 tsp vanilla extract\n1 tbsp coconut oil\n1 tsp cinnamon',
	        'instructions': '1. Preheat the oven to 325°F (165°C) and line a baking sheet with parchment paper.\n2. In a large bowl, combine rolled oats, chopped nuts, and cinnamon.\n3. In a small saucepan, warm honey, coconut oil, and vanilla extract until melted and combined.\n4. Pour the liquid mixture over the dry ingredients and stir until evenly coated.\n5. Spread the granola mixture onto the prepared baking sheet.\n6. Bake for 25–30 minutes, stirring halfway through, until golden brown.\n7. Let cool completely before storing in an airtight container.',
			'time': 40,
	        'meal_type': 'Breakfast',
			'image_url': 'https://cdn.loveandlemons.com/wp-content/uploads/2020/01/granola.jpg'
	    },
	    {
	        'title': 'Mango Sorbet',
	        'description': 'A refreshing, creamy sorbet made with pureed mango, perfect for a cool dessert.',
	        'ingredients': '2 ripe mangoes, peeled and chopped\n¼ cup sugar\n1 tbsp lime juice',
	        'instructions': '1. Place the chopped mangoes, sugar, and lime juice in a blender or food processor.\n2. Blend until smooth and creamy.\n3. Pour the mixture into an ice cream maker and churn according to the manufacturer’s instructions.\n4. If you don’t have an ice cream maker, pour the mixture into a shallow container and freeze, stirring every 30 minutes until smooth and frozen.\n5. Serve immediately or store in the freezer until ready to serve.',
			'time': 60,
	        'meal_type': 'Dessert',
			'image_url': 'https://myhomemaderecipe.com/assets/images/1735862992245-dw5m03b4.webp'
	    },
	    {
	        'title': 'Cucumber and Hummus Sandwiches',
	        'description': 'Refreshing cucumber slices and creamy hummus sandwiched between soft whole grain bread.',
	        'ingredients': '4 slices whole grain bread\n½ cucumber, thinly sliced\n¼ cup hummus\nLettuce (optional)',
	        'instructions': '1. Spread hummus evenly on each slice of whole grain bread.\n2. Layer thin cucumber slices on two of the bread slices.\n3. Add lettuce if desired.\n4. Top with the remaining slices of bread to form sandwiches.\n5. Cut in half and serve immediately.',
			'time': 15,
	        'meal_type': 'Lunch',
			'image_url': 'https://theyogafunk.com/wp-content/uploads/2024/07/ACUCUM2-1024x576.jpg'
	    },
	    {
	        'title': 'Oatmeal Raisin Cookies',
	        'description': 'Chewy oatmeal cookies filled with raisins and a touch of cinnamon, perfect for a quick snack or dessert.',
	        'ingredients': '1 ½ cups rolled oats\n¾ cup flour\n½ cup brown sugar\n½ cup raisins\n1 tsp cinnamon\n1 egg\n½ cup butter, softened\n1 tsp vanilla extract',
	        'instructions': '1. Preheat the oven to 350°F (175°C) and line a baking sheet with parchment paper.\n2. In a bowl, cream together softened butter and brown sugar until smooth.\n3. Beat in the egg and vanilla extract.\n4. In a separate bowl, combine flour, rolled oats, and cinnamon.\n5. Gradually mix the dry ingredients into the wet mixture.\n6. Fold in the raisins.\n7. Drop spoonfuls of dough onto the prepared baking sheet.\n8. Bake for 10–12 minutes, or until lightly golden.\n9. Let cool before serving.',
			'time': 30,
	        'meal_type': 'Dessert',
			'image_url': 'https://www.modernhoney.com/wp-content/uploads/2020/12/The-Best-Oatmeal-Raisin-Cookies-3-scaled.jpg'
	    },
	    {
	        'title': 'Spinach and Feta Stuffed Pita',
	        'description': 'A warm pita filled with spinach, feta, and a tangy yogurt dressing, perfect for lunch.',
	        'ingredients': '1 whole wheat pita\n1 cup spinach, wilted\n½ cup crumbled feta cheese\n2 tbsp plain yogurt\n1 tbsp lemon juice\nSalt and pepper',
	        'instructions': '1. Preheat the oven to 350°F (175°C) if you want the pita warm.\n2. In a bowl, mix the wilted spinach with crumbled feta cheese.\n3. In a small bowl, combine yogurt, lemon juice, salt, and pepper to make the dressing.\n4. Cut the pita in half to create pockets.\n5. Fill each pita pocket with the spinach and feta mixture.\n6. Drizzle the yogurt dressing over the filling.\n7. Warm the filled pita in the oven for 5–10 minutes if desired.\n8. Serve immediately.',
			'time': 30,
	        'meal_type': 'Lunch',
			'image_url': 'https://img.freepik.com/premium-photo/savory-spinach-feta-stuffed-pita_944420-7642.jpg'
	    },
	    {
	        'title': 'Peach Cobbler',
	        'description': 'A warm, fruity dessert with a buttery biscuit topping, perfect for summer.',
	        'ingredients': '4 peaches, sliced\n½ cup sugar\n1 tsp cinnamon\n1 tsp vanilla extract\n1 cup flour\n½ cup butter, cubed\n¾ cup milk',
	        'instructions': '1. Preheat the oven to 350°F (175°C) and grease a baking dish.\n2. In a bowl, mix sliced peaches with half of the sugar, cinnamon, and vanilla extract. Pour into the prepared baking dish.\n3. In a separate bowl, combine flour, remaining sugar, cubed butter, and milk. Stir until just combined to make the batter.\n4. Pour the batter over the peaches.\n5. Bake for 45–50 minutes, or until the topping is golden and cooked through.\n6. Let cool slightly before serving.',
			'time': 60,
	        'meal_type': 'Dessert',
			'image_url': 'https://joyfoodsunshine.com/wp-content/uploads/2020/05/peach-cobbler-recipe-7.jpg'
	    },
	    {
			"title": "Pandan Coconut Pancakes",
			"description": "Fluffy green pancakes with a subtle vanilla-like pandan aroma.",
			"ingredients": "Flour\nCoconut milk\nEggs\nPandan extract\nSugar\nBaking powder",
			"instructions": "1. In a bowl, whisk flour, sugar, and baking powder.\n2. Add eggs, coconut milk, and pandan extract.\n3. Mix until a smooth batter forms.\n4. Heat a non-stick pan and lightly grease it.\n5. Pour batter to form pancakes and cook until bubbles appear.\n6. Flip, cook briefly, and serve warm.",
			"time": 20,
			"meal_type": "breakfast",
			"image_url": "https://img.buzzfeed.com/thumbnailer-prod-us-east-1/video-api/assets/319191.jpg"
		},
		{
			"title": "Blueberry Oatmeal Bowl",
			"description": "A warm, comforting oatmeal bowl with blueberries and honey.",
			"ingredients": "Rolled oats\nBlueberries\nHoney\nMilk\nCinnamon",
			"instructions": "1. In a small pot, combine rolled oats and milk and cook over medium heat until the oats are soft and creamy.\n2. Stir in a pinch of cinnamon.\n3. Pour the oatmeal into a bowl.\n4. Top with fresh blueberries.\n5. Drizzle honey over the top.\n6. Serve warm.",
			"time": 10,
			"meal_type": "breakfast",
			"image_url": "https://lifemadesweeter.com/wp-content/uploads/Blueberry-Steel-Cut-Oats-Oatmeal-Bowl-photo-recipe-picture.jpg"
		},
		{
			"title": "Avocado Toast with Egg",
			"description": "Crispy toast topped with avocado and a perfectly cooked egg.",
			"ingredients": "Bread\nAvocado\nEgg\nSalt\nPepper\nLemon juice",
			"instructions": "1. Toast the bread slices until golden and crispy.\n2. Mash the avocado in a bowl and season with salt, pepper, and a squeeze of lemon juice.\n3. Spread the mashed avocado evenly on the toast.\n4. Cook the egg to your preferred style (fried, poached, or scrambled).\n5. Place the cooked egg on top of the avocado toast.\n6. Season with additional salt and pepper if desired and serve immediately.",
			"time": 8,
			"meal_type": "breakfast",
			"image_url": "https://www.skinnytaste.com/wp-content/uploads/2015/01/Avocado-Toast-with-Egg-3.jpg"
		},
		{
			"title": "Mediterranean Chickpea Salad",
			"description": "A bright salad with chickpeas, tomatoes, cucumbers, and herbs.",
			"ingredients": "Chickpeas\nCherry tomatoes\nCucumber\nRed onion\nOlive oil\nLemon\nParsley",
			"instructions": "1. In a large bowl, combine chickpeas, halved cherry tomatoes, diced cucumber, and finely chopped red onion.\n2. Drizzle with olive oil and squeeze fresh lemon juice over the salad.\n3. Add chopped parsley and season with salt and pepper.\n4. Toss everything together until well mixed.\n5. Serve immediately or chill for a few minutes before serving.",
			"time": 15,
			"meal_type": "lunch",
			"image_url": "https://quickprintrecipes.com/wp-content/uploads/2025/10/Mediterranean-Chickpea-Salad-2.jpg"
		},
		{
			"title": "Turkey and Hummus Wrap",
			"description": "A simple wrap filled with turkey, hummus, and crisp veggies.",
			"ingredients": "Tortilla\nTurkey slices\nHummus\nSpinach\nTomato\nCucumber",
			"instructions": "1. Lay the tortilla flat on a clean surface.\n2. Spread a layer of hummus evenly over the tortilla.\n3. Place turkey slices on top of the hummus.\n4. Add spinach, sliced tomato, and cucumber.\n5. Roll the tortilla tightly into a wrap.\n6. Slice in half and serve immediately.",
			"time": 10,
			"meal_type": "lunch",
			"image_url": "https://www.cannibalnyc.com/wp-content/uploads/2025/06/Turkey-and-Hummus-Wrap.jpg"
		},
		{
			"title": "Peruvian Ceviche",
			"description": "Fresh fish marinated in citrus juice with onion, chili, and cilantro.",
			"ingredients": "Fresh white fish\nLime juice\nRed onion\nChili pepper\nCilantro\nSalt\nSweet potato",
			"instructions": "1. Cut the fish into bite-sized cubes and place in a bowl.\n2. Season lightly with salt.\n3. Pour fresh lime juice over the fish until just covered.\n4. Add thinly sliced red onion and chopped chili pepper.\n5. Let marinate for a few minutes until the fish turns opaque.\n6. Garnish with chopped cilantro.\n7. Serve immediately, traditionally with cooked sweet potato on the side.",
			"time": 20,
			"meal_type": "dinner",
			"image_url": "https://www.enigmaperu.com/blog/wp-content/uploads/2018/06/CEVICHE.jpg"
		},
		{
			"title": "Yuzu Sesame Noodle Salad",
			"description": "Bright and refreshing noodles tossed with citrusy yuzu and nutty sesame.",
			"ingredients": "Soba noodles\nYuzu juice\nSesame oil\nSoy sauce\nSesame seeds\nGreen onions",
			"instructions": "1. Cook soba noodles according to package instructions.\n2. Drain and rinse noodles under cold water.\n3. In a bowl, whisk yuzu juice, soy sauce, and sesame oil.\n4. Toss noodles with the dressing.\n5. Sprinkle with sesame seeds and chopped green onions.\n6. Serve chilled or at room temperature.",
			"time": 15,
			"meal_type": "lunch",
			"image_url": "https://i0.wp.com/thefoodiediaries.co/wp-content/uploads/2021/06/img_5602-1.jpg?resize=800%2C800&ssl=1"
		},
		{
			"title": "Chocolate Chip Mug Cake",
			"description": "A quick, fluffy mug cake with chocolate chips.",
			"ingredients": "Flour\nSugar\nMilk\nOil\nChocolate chips\nVanilla extract",
			"instructions": "1. In a microwave-safe mug, combine flour, sugar, and a pinch of salt.\n2. Add milk, oil, and vanilla extract, stirring until smooth.\n3. Fold in chocolate chips.\n4. Microwave on high for 1–2 minutes, or until the cake has risen and is set in the middle.\n5. Let cool slightly before serving.",
			"time": 5,
			"meal_type": "dessert",
			"image_url": "https://insanelygoodrecipes.com/wp-content/uploads/2024/07/chocolate-chip-mug-cake-6.jpg"
		},
		{
			"title": "Berry Yogurt Parfait",
			"description": "Layers of yogurt, berries, and granola make a light snack.",
			"ingredients": "Greek yogurt\nStrawberries\nBlueberries\nGranola\nHoney",
			"instructions": "1. In a glass or bowl, spoon a layer of Greek yogurt.\n2. Add a layer of strawberries and blueberries.\n3. Sprinkle a layer of granola on top.\n4. Drizzle a little honey over the layers.\n5. Repeat layers if desired.\n6. Serve immediately.",
			"time": 7,
			"meal_type": "snack",
			"image_url": "https://mytriedrecipes.com/wp-content/uploads/2025/09/Berry_Yogurt_Parfait_wstkvy.webp"
		},
		{
			"title": "Dal Tadka",
			"description": "A comforting Indian lentil dish finished with a fragrant ghee tempering.",
			"ingredients": "Yellow lentils (toor or moong dal)\nGhee\nOnion\nTomato\nGarlic\nCumin seeds\nTurmeric\nSalt\nCilantro",
			"instructions": "1. Rinse the lentils thoroughly and cook them in water with turmeric and salt until soft.\n2. Mash the cooked lentils slightly and set aside.\n3. Heat ghee in a small pan over medium heat.\n4. Add cumin seeds and let them sizzle.\n5. Add chopped onion and sauté until golden.\n6. Stir in garlic and chopped tomato, cooking until soft.\n7. Pour the ghee mixture (tadka) over the cooked lentils and mix well.\n8. Garnish with chopped cilantro and serve warm.",
			"time": 30,
			"meal_type": "dinner",
			"image_url": "https://www.indianhealthyrecipes.com/wp-content/uploads/2021/04/dal-tadka-recipe.jpg"
		},
		{
			"title": "Tomato Basil Soup",
			"description": "A smooth tomato soup flavored with basil and garlic.",
			"ingredients": "Tomatoes\nBasil\nGarlic\nOnion\nOlive oil\nVegetable broth",
			"instructions": "1. Heat olive oil in a large pot over medium heat.\n2. Sauté chopped onion and minced garlic until soft and fragrant.\n3. Add chopped tomatoes and cook for 5–7 minutes.\n4. Pour in vegetable broth and bring to a simmer for 20 minutes.\n5. Stir in fresh basil leaves.\n6. Use an immersion blender to puree the soup until smooth.\n7. Season with salt and pepper to taste.\n8. Serve hot.",
			"time": 40,
			"meal_type": "dinner",
			"image_url": "https://lostinfood.co.uk/wp-content/uploads/2020/09/Tomato-Basil-Soup-4.jpg"
		},
		{
			"title": "Peanut Butter Banana Smoothie",
			"description": "A creamy smoothie with banana, peanut butter, and milk.",
			"ingredients": "Banana\nPeanut butter\nMilk\nHoney\nIce",
			"instructions": "1. In a blender, combine banana, peanut butter, milk, honey, and ice.\n2. Blend until smooth and creamy.\n3. Pour into a glass.\n4. Serve immediately.",
			"time": 5,
			"meal_type": "snack",
			"image_url": "https://lilluna.com/wp-content/uploads/2018/05/peanut-butter-banana-smoothie-9.jpg"
		},
		{
			"title": "Spaghetti Aglio e Olio",
			"description": "A simple pasta with garlic, olive oil, and chili flakes.",
			"ingredients": "Spaghetti\nGarlic\nOlive oil\nChili flakes\nParsley\nSalt",
			"instructions": "1. Cook the spaghetti according to package instructions until al dente. Drain and set aside.\n2. In a large skillet, heat olive oil over medium heat.\n3. Add thinly sliced garlic and sauté until golden and fragrant.\n4. Stir in chili flakes.\n5. Add the cooked spaghetti to the skillet and toss to coat in the garlic oil.\n6. Season with salt and chopped parsley.\n7. Serve immediately.",
			"time": 25,
			"meal_type": "dinner",
			"image_url": "https://cdn.loveandlemons.com/wp-content/uploads/2020/03/spaghetti-aglio-e-olio.jpg"
		},
		{
			"title": "Veggie Omelette",
			"description": "A fluffy omelette filled with colorful vegetables.",
			"ingredients": "Eggs\nSpinach\nBell peppers\nOnion\nSalt\nPepper",
			"instructions": "1. Beat the eggs in a bowl and season with salt and pepper.\n2. Heat a small amount of oil in a non-stick skillet over medium heat.\n3. Sauté chopped onion, bell peppers, and spinach until tender.\n4. Pour the beaten eggs over the vegetables in the skillet.\n5. Cook until the eggs begin to set, then gently fold the omelette.\n6. Cook for another 1–2 minutes until fully set.\n7. Slide onto a plate and serve immediately.",
			"time": 10,
			"meal_type": "breakfast",
			"image_url": "https://outsidemynest.com/wp-content/uploads/Healthy-Vegetable-Omelette-Recipe.jpg"
		},
		{
			"title": "Chicken Burrito Bowl",
			"description": "A hearty bowl with chicken, rice, beans, and veggies.",
			"ingredients": "Chicken\nRice\nBlack beans\nCorn\nTomatoes\nLettuce",
			"instructions": "1. Cook the rice according to package instructions.\n2. Season and cook the chicken until fully cooked, then dice or slice it.\n3. In a bowl, layer the cooked rice, black beans, corn, chopped tomatoes, and shredded lettuce.\n4. Top with the cooked chicken.\n5. Add any additional toppings or dressing as desired.\n6. Serve immediately.",
			"time": 35,
			"meal_type": "lunch",
			"image_url": "https://masonrecipes.com/wp-content/uploads/2025/01/Image_3-178.png"
		},
		{
			"title": "Garlic Butter Shrimp",
			"description": "Tender shrimp cooked quickly in garlic and butter.",
			"ingredients": "Shrimp\nGarlic\nButter\nLemon\nParsley\nSalt",
			"instructions": "1. Heat butter in a large skillet over medium heat.\n2. Add minced garlic and sauté until fragrant.\n3. Add the shrimp and cook for 2–3 minutes per side, until pink and opaque.\n4. Squeeze fresh lemon juice over the shrimp.\n5. Season with salt and sprinkle with chopped parsley.\n6. Serve immediately.",
			"time": 15,
			"meal_type": "dinner",
			"image_url": "https://www.jocooks.com/wp-content/uploads/2021/09/garlic-butter-shrimp-1-10.jpg"
		},
		{
			"title": "Saffron Rose Rice Pudding",
			"description": "Fragrant rice pudding infused with saffron threads and delicate rose aroma.",
			"ingredients": "Basmati rice\nMilk\nSaffron threads\nRose water\nSugar\nPistachios",
			"instructions": "1. Rinse the basmati rice and add it to a saucepan with milk.\n2. Simmer on low heat, stirring occasionally, until the rice is tender.\n3. Crush saffron threads and add them to the pudding.\n4. Stir in sugar and a few drops of rose water.\n5. Cook for another 5 minutes until creamy.\n6. Garnish with chopped pistachios and serve warm or chilled.",
			"time": 35,
			"meal_type": "dessert",
			"image_url": "https://img.freepik.com/premium-photo/saffron-scented-kheer-rice-pudding-nuts-rose-petals-topping_1003615-4793.jpg"
		},
		{
			"title": "Caprese Sandwich",
			"description": "Fresh mozzarella, tomato, and basil layered on crusty bread.",
			"ingredients": "Bread\nMozzarella\nTomato\nBasil\nOlive oil\nBalsamic",
			"instructions": "1. Slice the bread and drizzle with a little olive oil.\n2. Layer slices of fresh mozzarella and tomato on the bread.\n3. Add fresh basil leaves on top.\n4. Drizzle with balsamic vinegar.\n5. Close the sandwich with the other slice of bread.\n6. Serve immediately.",
			"time": 10,
			"meal_type": "lunch",
			"image_url": "https://www.somewhatsimple.com/wp-content/uploads/2015/07/caprese_sandwich_2.jpg"
		},
		{
			"title": "Banana Bread Squares",
			"description": "Soft banana bread cut into snackable squares.",
			"ingredients": "Bananas\nFlour\nSugar\nEggs\nButter\nBaking soda",
			"instructions": "1. Preheat the oven to 350°F (175°C) and grease a baking pan.\n2. Mash the bananas in a bowl.\n3. Mix in melted butter, sugar, and eggs until smooth.\n4. Add flour and baking soda, stirring until just combined.\n5. Pour the batter into the prepared pan.\n6. Bake for 35–40 minutes, or until a toothpick inserted in the center comes out clean.\n7. Let cool before cutting into squares and serving.",
			"time": 45,
			"meal_type": "snack",
			"image_url": "https://butternutbakeryblog.com/wp-content/uploads/2023/07/brown-butter-banana-bread-bars-683x1024.jpg"
		},
		{
			"title": "Lemon Bars",
			"description": "Bright, tangy lemon bars with a soft crust.",
			"ingredients": "Lemon juice\nSugar\nFlour\nButter\nEggs",
			"instructions": "1. Preheat the oven to 350°F (175°C) and grease a baking pan.\n2. In a bowl, mix flour, sugar, and melted butter to form the crust.\n3. Press the crust mixture into the bottom of the pan.\n4. Bake for 15–20 minutes until lightly golden.\n5. In another bowl, whisk together eggs, sugar, and lemon juice for the filling.\n6. Pour the filling over the baked crust.\n7. Bake for an additional 20–25 minutes until set.\n8. Let cool, then cut into bars and serve.",
			"time": 50,
			"meal_type": "dessert",
			"image_url": "https://www.jessicagavin.com/wp-content/uploads/2020/12/lemon-bars-27.jpg"
		},
		{
			"title": "Cucumber Mint Salad",
			"description": "A refreshing salad with cucumbers, mint, and lemon.",
			"ingredients": "Cucumbers\nMint\nLemon juice\nOlive oil\nSalt",
			"instructions": "1. Slice the cucumbers thinly and place them in a bowl.\n2. Chop fresh mint and add to the cucumbers.\n3. Drizzle with lemon juice and olive oil.\n4. Season with a pinch of salt.\n5. Toss everything together until well combined.\n6. Serve immediately or chill for a few minutes before serving.",
			"time": 8,
			"meal_type": "snack",
			"image_url": "https://www.homemademastery.com/wp-content/uploads/2024/07/cucumber-salad-with-mint-IMG_0117-735x1102.jpg"
		},
		{
			"title": "Baked Salmon with Dill",
			"description": "A simple baked salmon fillet seasoned with dill and lemon.",
			"ingredients": "Salmon\nDill\nLemon\nOlive oil\nSalt\nPepper",
			"instructions": "1. Preheat the oven to 400°F (200°C) and lightly grease a baking dish.\n2. Place the salmon fillet in the dish and drizzle with olive oil.\n3. Season with salt, pepper, and chopped fresh dill.\n4. Squeeze lemon juice over the salmon.\n5. Bake for 12–15 minutes, or until the salmon is cooked through and flakes easily.\n6. Serve immediately.",
			"time": 25,
			"meal_type": "dinner",
			"image_url": "https://ketocookingchristian.com/wp-content/uploads/2021/07/Baked-Salmon-with-Creamy-Dill-Sauce3-2-scaled.jpeg"
		},
		{
			"title": "Strawberry Cheesecake Cup",
			"description": "A quick layered cheesecake-style dessert in a cup.",
			"ingredients": "Cream cheese\nSugar\nStrawberries\nGraham crumbs\nVanilla",
			"instructions": "1. In a bowl, beat the cream cheese with sugar and a splash of vanilla until smooth.\n2. In serving cups, layer graham cracker crumbs at the bottom.\n3. Add a layer of the cream cheese mixture.\n4. Top with sliced strawberries.\n5. Repeat layers if desired.\n6. Serve immediately or chill for a few minutes before serving.",
			"time": 10,
			"meal_type": "dessert",
			"image_url": "https://diyjoy.com/wp-content/uploads/2023/04/no-bake-strawberry-cheesecake-cups-recipe.jpg"
		},
		{
			"title": "Bouillabaisse",
			"description": "Traditional Provençal fish stew made with assorted seafood and saffron.",
			"ingredients": "Assorted fish\nShellfish\nSaffron\nFennel\nTomatoes\nOlive oil\nGarlic",
			"instructions": "1. Sauté garlic and fennel in olive oil.\n2. Add tomatoes and saffron.\n3. Pour in water and simmer.\n4. Add firm fish first.\n5. Add delicate seafood last.\n6. Serve hot with bread.",
			"time": 120,
			"meal_type": "dinner",
			"image_url": "https://img.taste.com.au/xevn8hx3/taste/2016/11/bouillabaisse-78546-1.jpeg"
		},
		{
			"title": "Dolsot Bibimbap",
			"description": "Korean rice bowl topped with vegetables, egg, and gochujang.",
			"ingredients": "Rice\nSpinach\nBean sprouts\nCarrots\nEgg\nGochujang",
			"instructions": "1. Cook rice and keep warm.\n2. Sauté vegetables separately.\n3. Fry egg sunny-side up.\n4. Arrange toppings over rice.\n5. Add gochujang.\n6. Mix before eating.",
			"time": 45,
			"meal_type": "lunch",
			"image_url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Dolsot-bibimbap.jpg"
		}
	]

	return recipe_fixtures
