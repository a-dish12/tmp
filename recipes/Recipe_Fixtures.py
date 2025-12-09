def get_recipe_fixtures():
	recipe_fixtures = [
		{
	        'title': 'Avocado Toast with Poached Eggs',
	        'description': 'Creamy avocado on crispy toast, topped with a perfectly poached egg for a nutritious breakfast.',
	        'ingredients': '2 slices of whole grain bread\n1 ripe avocado\n2 large eggs\nSalt and pepper\nOlive oil (optional)\nRed pepper flakes (optional)',
	        'time': 15,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Classic Caesar Salad',
	        'description': 'A crispy romaine lettuce salad with tangy Caesar dressing, croutons, and parmesan cheese.',
	        'ingredients': '4 cups romaine lettuce\n½ cup Caesar dressing\n¼ cup grated parmesan\n½ cup croutons\nFresh ground black pepper',
	        'time': 10,
	        'meal_type': 'Lunch'
	    },
	    {
	        'title': 'Spaghetti Carbonara',
	        'description': 'A creamy, savory pasta with pancetta, eggs, and parmesan cheese. Perfectly comforting.',
	        'ingredients': '200g spaghetti\n100g pancetta\n2 large eggs\n1 cup grated parmesan\nSalt and pepper\n1 tbsp olive oil',
	        'time': 20,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Blueberry Muffins',
	        'description': 'Soft, fluffy muffins bursting with fresh blueberries, perfect for breakfast or a snack.',
	        'ingredients': '1 ½ cups all-purpose flour\n¾ cup sugar\n2 tsp baking powder\n1 tsp vanilla extract\n1 cup blueberries\n½ cup milk\n1 egg\n⅓ cup melted butter',
	        'time': 25,
	        'meal_type': 'Snack'
	    },
	    {
	        'title': 'Vegan Buddha Bowl',
	        'description': 'A colorful, nutrient-packed bowl with quinoa, roasted veggies, and a tahini dressing.',
	        'ingredients': '1 cup quinoa\n1 cup roasted sweet potatoes\n1 cup roasted broccoli\n½ cup chickpeas\n2 tbsp tahini\nLemon juice\nSalt and pepper',
	        'time': 40,
	        'meal_type': 'Lunch'
	    },
	    {
	        'title': 'Pancakes with Maple Syrup',
	        'description': 'Fluffy and golden pancakes served with a drizzle of maple syrup, a classic breakfast treat.',
	        'ingredients': '1 ½ cups all-purpose flour\n1 tbsp sugar\n1 tsp baking powder\n1 tsp vanilla extract\n1 cup milk\n2 eggs\n2 tbsp melted butter\nMaple syrup',
	        'time': 20,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Chicken Caesar Wrap',
	        'description': 'Grilled chicken, crispy romaine lettuce, and creamy Caesar dressing wrapped in a flour tortilla.',
	        'ingredients': '1 chicken breast, grilled and sliced\n1 large flour tortilla\n2 cups romaine lettuce\n¼ cup Caesar dressing\n¼ cup grated parmesan',
	        'time': 15,
	        'meal_type': 'Lunch'
	    },
	    {
	        'title': 'Vegetable Stir-Fry with Tofu',
	        'description': 'A quick and healthy stir-fry with tofu and assorted vegetables, served with rice.',
	        'ingredients': '1 block firm tofu, cubed\n1 cup broccoli florets\n1 bell pepper, sliced\n1 carrot, sliced\n2 tbsp soy sauce\n1 tbsp sesame oil\n1 cup cooked rice',
	        'time': 25,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Chocolate Chip Cookies',
	        'description': 'Soft, chewy cookies filled with gooey chocolate chips, the perfect dessert for any occasion.',
	        'ingredients': '1 ½ cups all-purpose flour\n1 tsp baking soda\n½ cup butter, softened\n¾ cup brown sugar\n½ cup granulated sugar\n1 tsp vanilla extract\n1 egg\n1 ½ cups chocolate chips',
	        'time': 30,
	        'meal_type': 'Dessert'
	    },
	    {
	        'title': 'Caprese Salad',
	        'description': 'Fresh mozzarella, tomatoes, and basil drizzled with olive oil and balsamic vinegar.',
	        'ingredients': '2 large tomatoes, sliced\n1 ball fresh mozzarella, sliced\n¼ cup fresh basil leaves\n2 tbsp olive oil\n1 tbsp balsamic vinegar\nSalt and pepper',
	        'time': 10,
	        'meal_type': 'Lunch'
	    },
	    {
	        'title': 'Shakshuka',
	        'description': 'A Middle Eastern dish of poached eggs in a spicy tomato and bell pepper sauce.',
	        'ingredients': '4 eggs\n2 cups diced tomatoes\n1 onion, chopped\n1 bell pepper, chopped\n2 cloves garlic, minced\n1 tsp cumin\n1 tsp paprika\nSalt and pepper\nOlive oil',
	        'time': 30,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Beef Tacos',
	        'description': 'Ground beef seasoned with taco spices, served in soft tortillas with toppings.',
	        'ingredients': '1 lb ground beef\n1 packet taco seasoning\n6 soft taco tortillas\n1 cup shredded lettuce\n1 cup diced tomatoes\n½ cup shredded cheddar cheese\nSour cream',
	        'time': 25,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Vegetable Soup',
	        'description': 'A warm and comforting soup filled with a variety of fresh vegetables.',
	        'ingredients': '2 cups diced potatoes\n2 carrots, chopped\n1 onion, chopped\n2 celery stalks, chopped\n2 cups vegetable broth\n1 cup green beans, chopped\n1 cup diced tomatoes\nSalt and pepper',
	        'time': 40,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Egg Salad Sandwich',
	        'description': 'Creamy egg salad made with mayonnaise and mustard, served between slices of bread.',
	        'ingredients': '4 boiled eggs, chopped\n2 tbsp mayonnaise\n1 tsp mustard\nSalt and pepper\n2 slices whole grain bread',
	        'time': 15,
	        'meal_type': 'Lunch'
	    },
	    {
	        'title': 'Grilled Cheese Sandwich',
	        'description': 'A classic grilled cheese sandwich with gooey melted cheese and crispy golden bread.',
	        'ingredients': '2 slices of bread\n2 slices of cheddar cheese\nButter',
	        'time': 10,
	        'meal_type': 'Snack'
	    },
	    {
	        'title': 'Salmon with Lemon and Dill',
	        'description': 'Baked salmon fillets topped with lemon and fresh dill for a light and healthy dinner.',
	        'ingredients': '2 salmon fillets\n1 lemon, sliced\n1 tbsp fresh dill, chopped\nSalt and pepper\nOlive oil',
	        'time': 25,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Pesto Pasta',
	        'description': 'Pasta tossed in a flavorful pesto sauce made from basil, garlic, pine nuts, and parmesan.',
	        'ingredients': '200g pasta\n¼ cup pesto sauce\n2 tbsp pine nuts, toasted\nParmesan cheese, grated',
	        'time': 20,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Smoothie Bowl',
	        'description': 'A thick, creamy smoothie topped with fresh fruit, granola, and seeds for extra crunch.',
	        'ingredients': '1 frozen banana\n½ cup frozen mixed berries\n½ cup almond milk\n¼ cup granola\nFresh fruit for topping (e.g., banana, strawberries)',
	        'time': 10,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Chicken Fried Rice',
	        'description': 'Stir-fried rice with chicken, vegetables, and soy sauce, an easy and delicious dinner option.',
	        'ingredients': '1 chicken breast, diced\n2 cups cooked rice\n1 cup frozen peas and carrots\n2 eggs, scrambled\n2 tbsp soy sauce\n1 tbsp sesame oil',
	        'time': 30,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Apple Cinnamon Oatmeal',
	        'description': 'A warm bowl of oatmeal topped with sautéed apples and cinnamon for a cozy breakfast.',
	        'ingredients': '1 cup rolled oats\n1 apple, diced\n1 tsp cinnamon\n1 tbsp honey\n1 cup milk',
	        'time': 15,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Buffalo Cauliflower Bites',
	        'description': 'Crispy roasted cauliflower coated in spicy buffalo sauce, a great vegetarian snack.',
	        'ingredients': '1 cauliflower head, cut into florets\n½ cup flour\n1 tsp garlic powder\n1 tsp paprika\n1 tsp onion powder\n½ cup buffalo sauce\nOlive oil',
	        'time': 30,
	        'meal_type': 'Snack'
	    },
	    {
	        'title': 'Chicken Shawarma',
	        'description': 'Tender chicken seasoned with shawarma spices, served in pita with garlic sauce and veggies.',
	        'ingredients': '2 chicken breasts, sliced\n1 tbsp shawarma seasoning\n1 tbsp olive oil\n2 pita breads\nGarlic sauce\nLettuce, tomatoes, cucumbers',
	        'time': 30,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Mango Sticky Rice',
	        'description': 'A sweet Thai dessert made with sticky rice, fresh mango, and a drizzle of coconut milk.',
	        'ingredients': '1 cup sticky rice\n1 ripe mango, sliced\n½ cup coconut milk\n2 tbsp sugar',
	        'time': 30,
	        'meal_type': 'Dessert'
	    },
	    {
	        'title': 'Beef Wellington',
	        'description': 'A rich and flavorful beef fillet wrapped in prosciutto, mushrooms, and puff pastry, baked to perfection.',
	        'ingredients': '1 lb beef tenderloin\n2 cups cremini mushrooms, chopped\n2 tbsp olive oil\n1 tbsp Dijon mustard\n8 oz prosciutto\n1 sheet puff pastry\n1 egg (for egg wash)\nSalt and pepper',
	        'time': 120,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Homemade Lasagna',
	        'description': 'Layers of pasta, rich tomato sauce, creamy ricotta, and melted mozzarella cheese, baked until bubbly.',
	        'ingredients': '12 lasagna noodles\n2 cups ricotta cheese\n1 lb ground beef\n1 jar marinara sauce\n1 onion, chopped\n1 tbsp garlic, minced\n2 cups mozzarella cheese\nParmesan cheese\n2 tbsp olive oil',
	        'time': 150,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Slow Cooker Beef Stew',
	        'description': 'Tender beef chunks, carrots, potatoes, and onions slow-cooked in a savory broth for a hearty meal.',
	        'ingredients': '2 lbs beef chuck, cut into cubes\n4 cups beef broth\n3 carrots, sliced\n3 potatoes, diced\n1 onion, chopped\n2 cloves garlic, minced\n1 tbsp thyme\n2 tbsp flour\nSalt and pepper',
	        'time': 180,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Chicken Parmesan',
	        'description': 'Breaded chicken breasts topped with marinara sauce and melted mozzarella cheese, served with spaghetti.',
	        'ingredients': '4 chicken breasts\n1 cup breadcrumbs\n1 cup flour\n2 eggs\n1 cup marinara sauce\n1 cup mozzarella cheese, shredded\n1 cup parmesan cheese, grated\n1 tbsp olive oil\nSpaghetti',
	        'time': 90,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Pulled Pork Sandwiches',
	        'description': 'Tender, slow-cooked pulled pork served with barbecue sauce and coleslaw on a soft bun.',
	        'ingredients': '3 lbs pork shoulder\n1 onion, sliced\n1 cup barbecue sauce\n2 tbsp brown sugar\n1 tbsp paprika\n1 tbsp garlic powder\n2 cups coleslaw mix\n4 buns',
	        'time': 180,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Homemade Croissants',
	        'description': 'Flaky, buttery croissants made from scratch with layers of dough and butter.',
	        'ingredients': '4 cups all-purpose flour\n1 tbsp sugar\n1 tsp salt\n2 tsp active dry yeast\n1 ¼ cups cold butter\n1 cup milk\n1 egg (for egg wash)',
	        'time': 240,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Beef Bourguignon',
	        'description': 'A French classic: tender beef braised in red wine with onions, mushrooms, and carrots, served over mashed potatoes.',
	        'ingredients': '2 lbs beef chuck, cut into cubes\n1 bottle red wine\n2 cups beef broth\n1 onion, chopped\n2 carrots, sliced\n2 cloves garlic, minced\n2 cups mushrooms, sliced\n2 tbsp flour\nSalt and pepper',
	        'time': 150,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Paella',
	        'description': 'A traditional Spanish dish made with saffron rice, seafood, chicken, and vegetables, cooked in one pan.',
	        'ingredients': '2 cups Arborio rice\n1 lb chicken thighs, diced\n1 lb shrimp, peeled\n1 cup peas\n1 red bell pepper, chopped\n2 tomatoes, chopped\n1 onion, chopped\n2 cloves garlic, minced\n1 tsp saffron threads\n4 cups chicken broth\nOlive oil',
	        'time': 120,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Braised Short Ribs',
	        'description': 'Tender, fall-off-the-bone short ribs braised in red wine and aromatics, served with mashed potatoes.',
	        'ingredients': '4 beef short ribs\n1 bottle red wine\n2 cups beef broth\n2 onions, chopped\n2 carrots, chopped\n2 cloves garlic, minced\n1 tbsp thyme\nSalt and pepper\nOlive oil',
	        'time': 180,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Roast Duck with Orange Glaze',
	        'description': 'A perfectly roasted duck with a sweet and tangy orange glaze, served with roasted vegetables.',
	        'ingredients': '1 whole duck\n2 oranges, juiced and zested\n1 tbsp honey\n2 tbsp soy sauce\n2 tbsp olive oil\n1 tbsp ginger, minced\n1 tbsp garlic, minced\nSalt and pepper\nRoasted vegetables (e.g., carrots, potatoes)',
	        'time': 150,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Chicken and Mushroom Risotto',
	        'description': 'A creamy and comforting risotto with tender chicken and earthy mushrooms, perfect for a cozy dinner.',
	        'ingredients': '1 lb chicken breast, diced\n1 cup Arborio rice\n1 cup sliced mushrooms\n1 onion, chopped\n2 cloves garlic, minced\n4 cups chicken broth\n1/2 cup dry white wine\n1/2 cup grated parmesan\nOlive oil\nSalt and pepper',
	        'time': 60,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Stuffed Bell Peppers',
	        'description': 'Colorful bell peppers stuffed with a savory mixture of ground beef, rice, tomatoes, and spices.',
	        'ingredients': '4 bell peppers, tops cut off and seeds removed\n1 lb ground beef\n1 cup cooked rice\n1 can diced tomatoes\n1 onion, chopped\n2 cloves garlic, minced\n1 tsp cumin\n1 tsp paprika\n1 cup shredded mozzarella cheese\nSalt and pepper',
	        'time': 75,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Chicken Fajitas',
	        'description': 'Sautéed chicken strips with bell peppers and onions, served with tortillas and your favorite toppings.',
	        'ingredients': '2 chicken breasts, sliced\n2 bell peppers, sliced\n1 onion, sliced\n2 tbsp fajita seasoning\n1 tbsp olive oil\n4 flour tortillas\nSour cream, guacamole, and salsa (optional)',
	        'time': 45,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Vegetable Lasagna',
	        'description': 'A hearty vegetarian lasagna made with layers of fresh vegetables, ricotta, and mozzarella cheese.',
	        'ingredients': '12 lasagna noodles\n2 cups ricotta cheese\n2 cups shredded mozzarella\n1 zucchini, sliced\n1 cup spinach\n1 cup sliced mushrooms\n1 jar marinara sauce\n1 onion, chopped\n1 tbsp olive oil\n1 tsp Italian seasoning',
	        'time': 90,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Grilled Lemon Herb Chicken',
	        'description': 'Tender grilled chicken marinated in lemon, garlic, and herbs, served with roasted vegetables.',
	        'ingredients': '4 chicken breasts\n1 lemon, juiced and zested\n3 cloves garlic, minced\n2 tbsp olive oil\n1 tsp dried oregano\n1 tsp dried thyme\nSalt and pepper\nRoasted vegetables (e.g., carrots, potatoes)',
	        'time': 60,
	        'meal_type': 'Dinner'
	    },
	    {
	        'title': 'Peanut Butter Energy Balls',
	        'description': 'No-bake energy balls made with peanut butter, oats, and honey, perfect for a quick snack.',
	        'ingredients': '1 cup rolled oats\n½ cup peanut butter\n¼ cup honey\n1 tbsp chia seeds\n1 tsp vanilla extract\n1 tbsp mini chocolate chips (optional)',
	        'time': 15,
	        'meal_type': 'Snack'
	    },
	    {
	        'title': 'Lemon Blueberry Muffins',
	        'description': 'Fluffy muffins with fresh blueberries and a zesty lemon flavor, great for breakfast or a snack.',
	        'ingredients': '1 ½ cups all-purpose flour\n¾ cup sugar\n1 tsp baking powder\n1 tsp baking soda\n1 cup blueberries\n1 tsp lemon zest\n1 egg\n1 cup buttermilk\n¼ cup butter, melted',
	        'time': 25,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Chocolate Avocado Mousse',
	        'description': 'A creamy, rich chocolate mousse made with ripe avocado for a healthier dessert.',
	        'ingredients': '2 ripe avocados\n¼ cup cocoa powder\n2 tbsp maple syrup\n1 tsp vanilla extract\nPinch of salt',
	        'time': 15,
	        'meal_type': 'Dessert'
	    },
	    {
	        'title': 'Vegetarian Tacos',
	        'description': 'Soft corn tortillas filled with seasoned black beans, avocado, lettuce, and salsa.',
	        'ingredients': '1 can black beans, drained and rinsed\n4 corn tortillas\n1 avocado, sliced\n1 cup lettuce, shredded\n1 tomato, diced\n1 tbsp taco seasoning\nSalsa',
	        'time': 30,
	        'meal_type': 'Lunch'
	    },
	    {
	        'title': 'Cinnamon Roll Pancakes',
	        'description': 'Fluffy pancakes with a cinnamon swirl, topped with icing for a decadent breakfast.',
	        'ingredients': '1 ½ cups pancake mix\n1 tsp cinnamon\n1 egg\n1 cup milk\n2 tbsp butter, melted\nFor the swirl: ¼ cup brown sugar, 1 tsp cinnamon\nFor the icing: ½ cup powdered sugar, 1 tbsp milk',
	        'time': 40,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Baked Apple Chips',
	        'description': 'Thinly sliced apples baked until crispy and lightly dusted with cinnamon, a healthy snack.',
	        'ingredients': '4 apples, thinly sliced\n1 tsp cinnamon\n1 tbsp sugar (optional)',
	        'time': 45,
	        'meal_type': 'Snack'
	    },
	    {
	        'title': 'Homemade Granola',
	        'description': 'Crunchy, sweet granola made with oats, honey, and nuts, perfect for breakfast or as a topping for yogurt.',
	        'ingredients': '3 cups rolled oats\n½ cup honey\n1 cup mixed nuts, chopped\n1 tsp vanilla extract\n1 tbsp coconut oil\n1 tsp cinnamon',
	        'time': 40,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Mango Sorbet',
	        'description': 'A refreshing, creamy sorbet made with pureed mango, perfect for a cool dessert.',
	        'ingredients': '2 ripe mangoes, peeled and chopped\n¼ cup sugar\n1 tbsp lime juice',
	        'time': 60,
	        'meal_type': 'Dessert'
	    },
	    {
	        'title': 'Cucumber and Hummus Sandwiches',
	        'description': 'Refreshing cucumber slices and creamy hummus sandwiched between soft whole grain bread.',
	        'ingredients': '4 slices whole grain bread\n½ cucumber, thinly sliced\n¼ cup hummus\nLettuce (optional)',
	        'time': 15,
	        'meal_type': 'Lunch'
	    },
	    {
	        'title': 'Banana Bread',
	        'description': 'Moist and fluffy banana bread with a hint of vanilla, perfect for breakfast or a snack.',
	        'ingredients': '2 ripe bananas, mashed\n1 cup sugar\n1 ½ cups all-purpose flour\n1 tsp baking powder\n1 tsp vanilla extract\n2 eggs\n½ cup butter, melted',
	        'time': 60,
	        'meal_type': 'Snack'
	    },
	    {
	        'title': 'Oatmeal Raisin Cookies',
	        'description': 'Chewy oatmeal cookies filled with raisins and a touch of cinnamon, perfect for a quick snack or dessert.',
	        'ingredients': '1 ½ cups rolled oats\n¾ cup flour\n½ cup brown sugar\n½ cup raisins\n1 tsp cinnamon\n1 egg\n½ cup butter, softened\n1 tsp vanilla extract',
	        'time': 30,
	        'meal_type': 'Dessert'
	    },
	    {
	        'title': 'Avocado Toast with Tomato',
	        'description': 'Creamy avocado spread on toasted bread, topped with sliced tomatoes and a sprinkle of sea salt.',
	        'ingredients': '2 slices whole grain bread\n1 ripe avocado\n1 tomato, sliced\nSalt and pepper\nOlive oil (optional)',
	        'time': 10,
	        'meal_type': 'Breakfast'
	    },
	    {
	        'title': 'Spinach and Feta Stuffed Pita',
	        'description': 'A warm pita filled with spinach, feta, and a tangy yogurt dressing, perfect for lunch.',
	        'ingredients': '1 whole wheat pita\n1 cup spinach, wilted\n½ cup crumbled feta cheese\n2 tbsp plain yogurt\n1 tbsp lemon juice\nSalt and pepper',
	        'time': 30,
	        'meal_type': 'Lunch'
	    },
	    {
	        'title': 'Peach Cobbler',
	        'description': 'A warm, fruity dessert with a buttery biscuit topping, perfect for summer.',
	        'ingredients': '4 peaches, sliced\n½ cup sugar\n1 tsp cinnamon\n1 tsp vanilla extract\n1 cup flour\n½ cup butter, cubed\n¾ cup milk',
	        'time': 60,
	        'meal_type': 'Dessert'
	    },
	    {
	        'title': 'Greek Yogurt Parfait',
	        'description': 'Layers of creamy Greek yogurt, honey, and fresh berries, topped with granola for crunch.',
	        'ingredients': '2 cups Greek yogurt\n2 tbsp honey\n1 cup fresh berries (strawberries, blueberries, etc.)\n½ cup granola',
	        'time': 15,
	        'meal_type': 'Breakfast'
	    }
	]

	return recipe_fixtures
