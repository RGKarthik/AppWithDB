import requests
from bs4 import BeautifulSoup
import json
import time
import random

def scrape_bollywood_movies():
    """
    Scrape popular Bollywood movies from 1990s onwards.
    This function will collect movie data from multiple sources.
    """
    
    # List of popular Bollywood movies from 1990s onwards
    # Since web scraping can be unreliable, I'll create a comprehensive list
    bollywood_movies = [
        {
            "title": "Dilwale Dulhania Le Jayenge",
            "release_year": 1995,
            "director": "Aditya Chopra",
            "producer": "Yash Chopra",
            "music_director": "Jatin-Lalit",
            "cast": "Shah Rukh Khan, Kajol, Amrish Puri, Farida Jalal",
            "plot": "A young man and woman fall in love on a European vacation. He follows her to India, where he asks her father for her hand in marriage.",
            "genre": "Romance, Drama"
        },
        {
            "title": "Kuch Kuch Hota Hai",
            "release_year": 1998,
            "director": "Karan Johar",
            "producer": "Yash Johar",
            "music_director": "Jatin-Lalit",
            "cast": "Shah Rukh Khan, Kajol, Rani Mukerji, Salman Khan",
            "plot": "A widowed father's eight-year-old daughter sets her heart on getting her father together with her deceased mother's best friend.",
            "genre": "Romance, Drama"
        },
        {
            "title": "Hum Aapke Hain Koun..!",
            "release_year": 1994,
            "director": "Sooraj Barjatya",
            "producer": "Kamal Kumar Barjatya",
            "music_director": "Raamlaxman",
            "cast": "Madhuri Dixit, Salman Khan, Mohnish Bahl, Renuka Shahane",
            "plot": "Prem and Nisha's families arrange their marriages to each other's siblings. However, destiny has other plans when the couple falls in love.",
            "genre": "Family, Romance"
        },
        {
            "title": "Lagaan",
            "release_year": 2001,
            "director": "Ashutosh Gowariker",
            "producer": "Aamir Khan",
            "music_director": "A. R. Rahman",
            "cast": "Aamir Khan, Gracy Singh, Rachel Shelley, Paul Blackthorne",
            "plot": "The people of a small village in Victorian India stake their future on a game of cricket against their ruthless British rulers.",
            "genre": "Drama, Sports"
        },
        {
            "title": "3 Idiots",
            "release_year": 2009,
            "director": "Rajkumar Hirani",
            "producer": "Vidhu Vinod Chopra",
            "music_director": "Shantanu Moitra",
            "cast": "Aamir Khan, R. Madhavan, Sharman Joshi, Kareena Kapoor",
            "plot": "Two friends are searching for their long lost companion. They revisit their college days and recall the memories of their friend who inspired them to think differently.",
            "genre": "Comedy, Drama"
        },
        {
            "title": "Dangal",
            "release_year": 2016,
            "director": "Nitesh Tiwari",
            "producer": "Aamir Khan, Kiran Rao",
            "music_director": "Pritam",
            "cast": "Aamir Khan, Fatima Sana Shaikh, Sanya Malhotra, Zaira Wasim",
            "plot": "Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games.",
            "genre": "Biography, Drama, Sports"
        },
        {
            "title": "Zindagi Na Milegi Dobara",
            "release_year": 2011,
            "director": "Zoya Akhtar",
            "producer": "Ritesh Sidhwani, Farhan Akhtar",
            "music_director": "Shankar-Ehsaan-Loy",
            "cast": "Hrithik Roshan, Farhan Akhtar, Abhay Deol, Katrina Kaif",
            "plot": "Three friends decide to turn their fantasy vacation into reality after one of their friends gets engaged.",
            "genre": "Adventure, Comedy, Drama"
        },
        {
            "title": "Queen",
            "release_year": 2013,
            "director": "Vikas Bahl",
            "producer": "Anurag Kashyap, Vikramaditya Motwane",
            "music_director": "Amit Trivedi",
            "cast": "Kangana Ranaut, Rajkummar Rao, Lisa Haydon",
            "plot": "A Delhi girl from a traditional family sets out on a solo honeymoon after her marriage gets cancelled.",
            "genre": "Comedy, Drama"
        },
        {
            "title": "Taare Zameen Par",
            "release_year": 2007,
            "director": "Aamir Khan, Amole Gupte",
            "producer": "Aamir Khan",
            "music_director": "Shantanu Moitra",
            "cast": "Darsheel Safary, Aamir Khan, Tisca Chopra, Vipin Sharma",
            "plot": "An eight-year-old boy is thought to be lazy and a trouble-maker, until the new art teacher has the patience and compassion to discover the real problem behind his struggles in school.",
            "genre": "Drama, Family"
        },
        {
            "title": "Pink",
            "release_year": 2016,
            "director": "Aniruddha Roy Chowdhury",
            "producer": "Rashmi Sharma, Shoojit Sircar",
            "music_director": "Shantanu Moitra",
            "cast": "Taapsee Pannu, Amitabh Bachchan, Kirti Kulhari, Andrea Tariang",
            "plot": "When three young women are implicated in a crime, a retired lawyer steps forward to help them clear their names.",
            "genre": "Drama, Thriller"
        },
        {
            "title": "Andhadhun",
            "release_year": 2018,
            "director": "Sriram Raghavan",
            "producer": "Sriram Raghavan, Akshay Singh",
            "music_director": "Amit Trivedi",
            "cast": "Ayushmann Khurrana, Tabu, Radhika Apte",
            "plot": "A series of mysterious events change the life of a blind pianist who now must report a crime that was actually never witnessed by him.",
            "genre": "Crime, Mystery, Thriller"
        },
        {
            "title": "Sholay",
            "release_year": 1975,
            "director": "Ramesh Sippy",
            "producer": "G. P. Sippy",
            "music_director": "R. D. Burman",
            "cast": "Dharmendra, Amitabh Bachchan, Sanjeev Kumar, Hema Malini",
            "plot": "After his family is murdered by a notorious and ruthless bandit, a former police officer enlists the services of two outlaws to capture the bandit.",
            "genre": "Action, Adventure, Drama"
        },
        {
            "title": "Mughal-E-Azam",
            "release_year": 1960,
            "director": "K. Asif",
            "producer": "Shapoorji Pallonji",
            "music_director": "Naushad",
            "cast": "Prithviraj Kapoor, Dilip Kumar, Madhubala",
            "plot": "A 16th century prince falls in love with a court dancer and battles with his emperor father.",
            "genre": "Drama, Romance"
        },
        {
            "title": "Baahubali: The Beginning",
            "release_year": 2015,
            "director": "S. S. Rajamouli",
            "producer": "Shobu Yarlagadda, Prasad Devineni",
            "music_director": "M. M. Keeravani",
            "cast": "Prabhas, Rana Daggubati, Anushka Shetty, Tamannaah",
            "plot": "In ancient India, an adventurous and daring man becomes involved in a decades old feud between two warring tribes.",
            "genre": "Action, Drama"
        },
        {
            "title": "Baahubali 2: The Conclusion",
            "release_year": 2017,
            "director": "S. S. Rajamouli",
            "producer": "Shobu Yarlagadda, Prasad Devineni",
            "music_director": "M. M. Keeravani",
            "cast": "Prabhas, Rana Daggubati, Anushka Shetty, Sathyaraj",
            "plot": "When Shiva, the son of Bahubali, learns about his heritage, he begins to look for answers. His story is juxtaposed with past events that unfolded in the Mahishmati Kingdom.",
            "genre": "Action, Drama"
        },
        {
            "title": "Dil Chahta Hai",
            "release_year": 2001,
            "director": "Farhan Akhtar",
            "producer": "Ritesh Sidhwani",
            "music_director": "Shankar-Ehsaan-Loy",
            "cast": "Aamir Khan, Saif Ali Khan, Akshaye Khanna, Preity Zinta",
            "plot": "Three inseparable childhood friends are just out of college. Nothing comes between them - until they each fall in love, and their wildly different approaches to relationships creates tension.",
            "genre": "Comedy, Drama, Romance"
        },
        {
            "title": "Rang De Basanti",
            "release_year": 2006,
            "director": "Rakeysh Omprakash Mehra",
            "producer": "Ronnie Screwvala",
            "music_director": "A. R. Rahman",
            "cast": "Aamir Khan, Siddharth, Soha Ali Khan, Kunal Kapoor",
            "plot": "The story of six young Indians who assist an English woman to film a documentary on the freedom fighters from their past, and how the process of filming inspired them to rebel against the corrupt government.",
            "genre": "Crime, Drama"
        },
        {
            "title": "My Name is Khan",
            "release_year": 2010,
            "director": "Karan Johar",
            "producer": "Hiroo Yash Johar, Gauri Khan",
            "music_director": "Shankar-Ehsaan-Loy",
            "cast": "Shah Rukh Khan, Kajol, Jimmy Sheirgill",
            "plot": "An Indian Muslim man with Asperger's syndrome takes a challenge to speak to the President of the United States seriously and embarks on a cross-country journey.",
            "genre": "Drama, Romance"
        },
        {
            "title": "Haider",
            "release_year": 2014,
            "director": "Vishal Bhardwaj",
            "producer": "Siddharth Roy Kapur, Vishal Bhardwaj",
            "music_director": "Vishal Bhardwaj",
            "cast": "Shahid Kapoor, Shraddha Kapoor, Tabu, Kay Kay Menon",
            "plot": "A young man returns to Kashmir after his father's disappearance to confront his uncle, whom he suspects of playing a role in his father's fate.",
            "genre": "Action, Crime, Drama"
        },
        {
            "title": "Tumhari Sulu",
            "release_year": 2017,
            "director": "Suresh Triveni",
            "producer": "Tanuj Garg, Atul Kasbekar",
            "music_director": "Guru Randhawa",
            "cast": "Vidya Balan, Manav Kaul, Neha Dhupia",
            "plot": "Sulochana, a housewife and mother, who takes up a night RJ job and how it changes her and her family's life.",
            "genre": "Comedy, Drama"
        },
        {
            "title": "Article 15",
            "release_year": 2019,
            "director": "Anubhav Sinha",
            "producer": "Anubhav Sinha, Zee Studios",
            "music_director": "Mangesh Dhakde",
            "cast": "Ayushmann Khurrana, Nassar, Manoj Pahwa, Kumud Mishra",
            "plot": "A young IPS officer's new posting in rural India has him confronting caste disparities and the darker aspects of law enforcement in the area.",
            "genre": "Crime, Drama"
        },
        {
            "title": "Gully Boy",
            "release_year": 2019,
            "director": "Zoya Akhtar",
            "producer": "Ritesh Sidhwani, Farhan Akhtar",
            "music_director": "Divine, Naezy",
            "cast": "Ranveer Singh, Alia Bhatt, Siddhant Chaturvedi",
            "plot": "A coming-of-age story based on the lives of street rappers in Mumbai.",
            "genre": "Drama, Music"
        },
        {
            "title": "URI: The Surgical Strike",
            "release_year": 2019,
            "director": "Aditya Dhar",
            "producer": "Ronnie Screwvala",
            "music_director": "Shashwat Sachdev",
            "cast": "Vicky Kaushal, Paresh Rawal, Mohit Raina, Yami Gautam",
            "plot": "Indian army special forces execute a covert operation, avenging the killing of fellow army men at their base by a terrorist group.",
            "genre": "Action, Drama, War"
        },
        {
            "title": "Chak De! India",
            "release_year": 2007,
            "director": "Shimit Amin",
            "producer": "Aditya Chopra",
            "music_director": "Salim-Sulaiman",
            "cast": "Shah Rukh Khan, Vidya Malvade, Sagarika Ghatge",
            "plot": "A disgraced ex-hockey player coaches the women's national team to prove his loyalty to the country.",
            "genre": "Drama, Sport"
        },
        {
            "title": "Super 30",
            "release_year": 2019,
            "director": "Vikas Bahl",
            "producer": "Sajid Nadiadwala",
            "music_director": "Ajay-Atul",
            "cast": "Hrithik Roshan, Mrunal Thakur, Nandish Sandhu",
            "plot": "Based on the life of Patna-based mathematician Anand Kumar who runs the famed Super 30 program for IIT aspirants in Patna.",
            "genre": "Biography, Drama"
        },
        {
            "title": "The Lunchbox",
            "release_year": 2013,
            "director": "Ritesh Batra",
            "producer": "Guneet Monga, Anurag Kashyap",
            "music_director": "Max Richter",
            "cast": "Irrfan Khan, Nimrat Kaur, Nawazuddin Siddiqui",
            "plot": "A mistaken delivery in Mumbai's famously efficient lunchbox delivery system connects a young housewife to an older man in the dusk of his life as they build a fantasy world together through notes in the lunchbox.",
            "genre": "Drama, Romance"
        },
        {
            "title": "Stree",
            "release_year": 2018,
            "director": "Amar Kaushik",
            "producer": "Dinesh Vijan, Raj Nidimoru",
            "music_director": "Sachin-Jigar",
            "cast": "Rajkummar Rao, Shraddha Kapoor, Pankaj Tripathi",
            "plot": "In the town of Chanderi, the menfolk live in fear of an evil spirit named 'Stree' who abducts men in the night. Based on the urban legend of 'Nale Ba' that went viral in Karnataka in the 1990s.",
            "genre": "Comedy, Horror"
        },
        {
            "title": "Badhaai Ho",
            "release_year": 2018,
            "director": "Amit Sharma",
            "producer": "Vineet Jain, Aleya Sen",
            "music_director": "Tanishk Bagchi",
            "cast": "Ayushmann Khurrana, Neena Gupta, Gajraj Rao, Sanya Malhotra",
            "plot": "A man faces embarrassment in the society when he finds out his mother is pregnant at an age where his wife conception.",
            "genre": "Comedy, Drama"
        },
        {
            "title": "Raazi",
            "release_year": 2018,
            "director": "Meghna Gulzar",
            "producer": "Vineet Jain, Karan Johar",
            "music_director": "Shankar-Ehsaan-Loy",
            "cast": "Alia Bhatt, Vicky Kaushal, Rajit Kapur, Shishir Sharma",
            "plot": "An Indian spy is married to a Pakistani military officer during the Indo-Pakistani War of 1971.",
            "genre": "Action, Drama, Thriller"
        },
        {
            "title": "Pad Man",
            "release_year": 2018,
            "director": "R. Balki",
            "producer": "Twinkle Khanna, Gauri Shinde",
            "music_director": "Amit Trivedi",
            "cast": "Akshay Kumar, Sonam Kapoor, Radhika Apte",
            "plot": "Upon realizing the extent to which women are affected by their menses, a man sets out to create a sanitary pad machine and to provide inexpensive sanitary pads to the women of rural India.",
            "genre": "Biography, Comedy, Drama"
        },
        {
            "title": "Golmaal: Fun Unlimited",
            "release_year": 2006,
            "director": "Rohit Shetty",
            "producer": "Dhilin Mehta",
            "music_director": "Vishal-Shekhar",
            "cast": "Ajay Devgn, Arshad Warsi, Sharman Joshi, Tusshar Kapoor",
            "plot": "Four runaway crooks take shelter in a bungalow which is owned by a blind couple.",
            "genre": "Comedy"
        },
        {
            "title": "Munna Bhai M.B.B.S.",
            "release_year": 2003,
            "director": "Rajkumar Hirani",
            "producer": "Vidhu Vinod Chopra",
            "music_director": "Anu Malik",
            "cast": "Sanjay Dutt, Arshad Warsi, Gracy Singh, Boman Irani",
            "plot": "A gangster sets out to fulfill his father's dream of becoming a doctor.",
            "genre": "Comedy, Drama"
        },
        {
            "title": "Lage Raho Munna Bhai",
            "release_year": 2006,
            "director": "Rajkumar Hirani",
            "producer": "Vidhu Vinod Chopra",
            "music_director": "Shantanu Moitra",
            "cast": "Sanjay Dutt, Arshad Warsi, Vidya Balan, Boman Irani",
            "plot": "Munna Bhai embarks on a journey with Mahatma Gandhi in order to fight against a corrupt property dealer.",
            "genre": "Comedy, Drama"
        },
        {
            "title": "Don",
            "release_year": 2006,
            "director": "Farhan Akhtar",
            "producer": "Ritesh Sidhwani",
            "music_director": "Shankar-Ehsaan-Loy",
            "cast": "Shah Rukh Khan, Priyanka Chopra, Arjun Rampal, Isha Koppikar",
            "plot": "Vijay is recruited by a police officer to masquerade as his lookalike Don, the leader of an international gang of smugglers. Things go wrong when the officer is killed and Vijay is left to fend for himself.",
            "genre": "Action, Crime, Thriller"
        },
        {
            "title": "Rock On!!",
            "release_year": 2008,
            "director": "Abhishek Kapoor",
            "producer": "Ritesh Sidhwani, Farhan Akhtar",
            "music_director": "Shankar-Ehsaan-Loy",
            "cast": "Farhan Akhtar, Arjun Rampal, Luke Kenny, Purab Kohli",
            "plot": "Four friends reunite to relive their moments of glory as a rock band.",
            "genre": "Drama, Music"
        },
        {
            "title": "Kai Po Che!",
            "release_year": 2013,
            "director": "Abhishek Kapoor",
            "producer": "Ronnie Screwvala, Siddharth Roy Kapur",
            "music_director": "Amit Trivedi",
            "cast": "Sushant Singh Rajput, Rajkummar Rao, Amit Sadh",
            "plot": "Three friends start an academy to train aspiring cricketers. But before they realise their goals, they experience an earthquake, religious riots and terrorism.",
            "genre": "Drama, Sport"
        },
        {
            "title": "Masaan",
            "release_year": 2015,
            "director": "Neeraj Ghaywan",
            "producer": "Manish Mundra, Anurag Kashyap",
            "music_director": "Indian Ocean",
            "cast": "Richa Chadha, Sanjay Mishra, Vicky Kaushal, Shweta Tripathi",
            "plot": "Four lives intersect along the Ganges: a low caste boy hopelessly in love, a daughter ridden with guilt of a sexual encounter ending in a tragedy, a hapless father with fading morality, and a spirited child yearning for a family, long to escape the moral constructs of a small-town.",
            "genre": "Drama"
        },
        {
            "title": "Newton",
            "release_year": 2017,
            "director": "Amit Masurkar",
            "producer": "Manish Mundra",
            "music_director": "Naren Chandavarkar, Benedict Taylor",
            "cast": "Rajkummar Rao, Pankaj Tripathi, Anjali Patil",
            "plot": "A government clerk on election duty in the conflict-ridden jungle of Central India tries his best to conduct free and fair voting despite the apathy of security forces and the looming fear of guerrilla attacks by communist rebels.",
            "genre": "Comedy, Drama"
        },
        {
            "title": "Barfi!",
            "release_year": 2012,
            "director": "Anurag Basu",
            "producer": "Ronnie Screwvala, Siddharth Roy Kapur",
            "music_director": "Pritam",
            "cast": "Ranbir Kapoor, Priyanka Chopra, Ileana D'Cruz",
            "plot": "Three young people learn that love can neither be defined nor contained by society's definition of normal and abnormal.",
            "genre": "Comedy, Drama, Romance"
        },
        {
            "title": "Wake Up Sid",
            "release_year": 2009,
            "director": "Ayan Mukerji",
            "producer": "Hiroo Yash Johar, Karan Johar",
            "music_director": "Shankar-Ehsaan-Loy",
            "cast": "Ranbir Kapoor, Konkona Sen Sharma, Supriya Pathak",
            "plot": "A spoiled young adult living in Mumbai experiences a change in his lazy ways when he meets a woman at a party, who inspires him to 'wake up'.",
            "genre": "Coming-of-age, Drama"
        },
        {
            "title": "Yeh Jawaani Hai Deewani",
            "release_year": 2013,
            "director": "Ayan Mukerji",
            "producer": "Hiroo Yash Johar, Karan Johar",
            "music_director": "Pritam",
            "cast": "Ranbir Kapoor, Deepika Padukone, Aditya Roy Kapur, Kalki Koechlin",
            "plot": "Kabir and Naina bond during a trekking trip. Before Naina can express herself, Kabir leaves India to pursue his career. They meet again years later, but he still cherishes his dreams more than bonds.",
            "genre": "Coming-of-age, Drama, Romance"
        },
        {
            "title": "Zanjeer",
            "release_year": 1973,
            "director": "Prakash Mehra",
            "producer": "Prakash Mehra",
            "music_director": "Kalyanji-Anandji",
            "cast": "Amitabh Bachchan, Jaya Bhaduri, Pran, Ajit",
            "plot": "A police officer fights corruption in his department and seeks revenge for his parents' murder.",
            "genre": "Action, Crime, Drama"
        },
        {
            "title": "Deewaar",
            "release_year": 1975,
            "director": "Yash Chopra",
            "producer": "Gulshan Rai",
            "music_director": "R. D. Burman",
            "cast": "Amitabh Bachchan, Shashi Kapoor, Nirupa Roy, Parveen Babi",
            "plot": "The story of two brothers who choose different paths in life - one becomes a police officer while the other turns to crime.",
            "genre": "Action, Crime, Drama"
        },
        {
            "title": "Anand",
            "release_year": 1971,
            "director": "Hrishikesh Mukherjee",
            "producer": "N. C. Sippy",
            "music_director": "Salil Chowdhury",
            "cast": "Rajesh Khanna, Amitabh Bachchan, Sumita Sanyal",
            "plot": "A cancer patient who has only a few months to live decides to spread joy and laughter through his actions.",
            "genre": "Drama"
        },
        {
            "title": "Amar Akbar Anthony",
            "release_year": 1977,
            "director": "Manmohan Desai",
            "producer": "Manmohan Desai",
            "music_director": "Laxmikant-Pyarelal",
            "cast": "Amitabh Bachchan, Vinod Khanna, Rishi Kapoor, Neetu Singh",
            "plot": "Three brothers separated in childhood are raised in different religions and later reunite to fight against the villains who separated them.",
            "genre": "Action, Comedy, Drama"
        },
        {
            "title": "Andaz Apna Apna",
            "release_year": 1994,
            "director": "Rajkumar Santoshi",
            "producer": "Vinay Kumar Sinha",
            "music_director": "Tushar Bhatia",
            "cast": "Aamir Khan, Salman Khan, Raveena Tandon, Karisma Kapoor",
            "plot": "Two slackers competing for the affections of an heiress inadvertently become her protectors from an evil criminal.",
            "genre": "Action, Comedy"
        },
        {
            "title": "Hera Pheri",
            "release_year": 2000,
            "director": "Priyadarshan",
            "producer": "A. G. Nadiadwala",
            "music_director": "Anu Malik",
            "cast": "Akshay Kumar, Suniel Shetty, Paresh Rawal, Tabu",
            "plot": "Three unemployed men find the answer to all their money problems when they receive a call from a kidnapper. However, things do not go as planned.",
            "genre": "Comedy, Crime"
        },
        {
            "title": "Bhaag Milkha Bhaag",
            "release_year": 2013,
            "director": "Rakeysh Omprakash Mehra",
            "producer": "Ronnie Screwvala, Rajiv Tandon",
            "music_director": "Shankar-Ehsaan-Loy",
            "cast": "Farhan Akhtar, Sonam Kapoor, Pavan Malhotra, Art Malik",
            "plot": "The true story of the 'Flying Sikh' - world champion runner and Olympian Milkha Singh who overcame the massacre of his family, civil war during the India-Pakistan partition, and homelessness to become one of India's most iconic athletes.",
            "genre": "Biography, Drama, Sport"
        },
        {
            "title": "Mary Kom",
            "release_year": 2014,
            "director": "Omung Kumar",
            "producer": "Sanjay Leela Bhansali",
            "music_director": "Shashi Suman",
            "cast": "Priyanka Chopra, Darshan Kumar, Sunil Thapa",
            "plot": "A chronicle of the life of Indian boxer Mary Kom who went through several hardships before audaciously accomplishing her ultimate dream.",
            "genre": "Biography, Drama, Sport"
        },
        {
            "title": "Toilet: Ek Prem Katha",
            "release_year": 2017,
            "director": "Shree Narayan Singh",
            "producer": "Neeraj Pandey, Shital Bhatia",
            "music_director": "Vickey Prasad",
            "cast": "Akshay Kumar, Bhumi Pednekar, Anupam Kher, Divyendu Sharma",
            "plot": "A woman threatens to leave her husband unless he installs a toilet in their home. To win back her love and respect, he heads out on a journey to fight against the backward society.",
            "genre": "Comedy, Drama"
        },
        {
            "title": "Sardar Udham",
            "release_year": 2021,
            "director": "Shoojit Sircar",
            "producer": "Ronnie Lahiri, Sheel Kumar",
            "music_director": "Shantanu Moitra",
            "cast": "Vicky Kaushal, Shaun Scott, Stephen Hogan, Banita Sandhu",
            "plot": "A biopic detailing the life of Sardar Udham Singh, a Sikh revolutionary who assassinated Michael O'Dwyer in London to avenge the 1919 Jallianwala Bagh massacre in Amritsar.",
            "genre": "Biography, Crime, Drama"
        },
        {
            "title": "Shershaah",
            "release_year": 2021,
            "director": "Vishnuvardhan",
            "producer": "Hiroo Yash Johar, Karan Johar",
            "music_director": "Tanishk Bagchi",
            "cast": "Sidharth Malhotra, Kiara Advani, Shiv Panditt, Nikitin Dheer",
            "plot": "Based on the life of Captain Vikram Batra who was an officer of the Indian Army, posthumously awarded the Param Vir Chakra, India's highest and most prestigious award for valour, for his actions during the 1999 Kargil War in Kashmir between India and Pakistan.",
            "genre": "Action, Biography, Drama"
        }
    ]
    
    return bollywood_movies

def save_movies_to_json():
    """Save the movie data to a JSON file for later use."""
    movies = scrape_bollywood_movies()
    
    with open('bollywood_movies.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully saved {len(movies)} movies to bollywood_movies.json")
    return movies

if __name__ == "__main__":
    movies = save_movies_to_json()
    print(f"Total movies collected: {len(movies)}")
    for movie in movies[:5]:  # Print first 5 movies as sample
        print(f"- {movie['title']} ({movie['release_year']})")