1. **Web Crawler**

    Run *crawler.py* :
    
        python crawler.py --url http://python.aori.ru/ --size 5
    
    The script will generate file *database.json*

2. **Graph**
    
    Visualize data retrieved by *crawler.py*
    
    Run *database_graph.py* : 
    
        python database_graph.py --filename database.json

    The script will generate an image *network.png*

3. **vk.com APIs**
    
    You can get audios of a given user or see how many audios each of his/her friends has.

    Edit *config.example.py* with your data and rename it to *config.py*. If you have your access token you don't need to fill remaining fields.
    
    Run *vk_audios.py* : 
    
        python vk_audios.py --user_id user_id

4. **Letters frequency visualized**

    Run *letters_frequency.py* :
    
        python letters_frequency.py --filename your_file 

5. **Tests**

    Run all tests and calculate test coverage:
    
        py.test test/ --cov=.

You can use this [Vagrant box rar] (https://www.dropbox.com/s/ffba7i5cye6w03t/testbox.rar?dl=0) or [Vagrant box tarball] (https://www.dropbox.com/s/t0brr0sulweox10/testbox.tar.gz?dl=0) to test the scripts.