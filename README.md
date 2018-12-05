# Activity Catalog Application

### This application was developed as a project for the FullStack Udacity Nanodegree program. It provides a list of activities separated by season. It uses Google for authentication, which allows users to create, edit and delete new activities.

This repo includes the HTML, CSS and python files used to start the applications. In order to install all Python the dependencies, please execute the following command.

```
$ pip install -r requirements.txt
```

To run the application, you are required to have your own Google API secrets. To get started, please go to this [link](https://console.developers.google.com/apis/credentials). Detailed documentation can be found [here](https://developers.google.com/identity/protocols/OAuth2). The activity catalog application requires that the `Authorized JavaScript origins` and the `Authorized redirect URIs` are set.

Once you have successfully created your cretendials, please download the JSON file from Google and name it `client_secrets.json`. A sample file is included in this repo for reference. 

To initialize the database run:

```
$ python database_setup.py 
```

If you want to add some data examples, please run:

```
$ python lotsofitems.py
```

Finally, to execute the application, please run:

```
$ python application.py
```

To test the application in your local machine, please visit [http://localhost:5000/](http://localhost:5000/). This will lead you to the main page. From there you can explore the different categories. For instance, if you loaded the sample data into the database, [http://localhost:5000/categories/3/items/](http://localhost:5000/categories/3/items/) will lead you to the Fall Activities category, and show you a list that include gymnastics, fencing and drama. From this site, you can also choose to create a new item, edit one or delete one. 

Additionally, the application also includes JSON endpoints that would dump different contents from the database into JSON format. For example, [http://localhost:5000/categories/JSON](http://localhost:5000/categories/JSON) presents the following output:

```
{
  "categories": [
    {
      "id": 1, 
      "name": "Summer"
    }, 
    {
      "id": 2, 
      "name": "Winter"
    }, 
    {
      "id": 3, 
      "name": "Fall"
    }, 
    {
      "id": 4, 
      "name": "Spring"
    }
  ]
}
```
 
Similarly, the endpoints [http://localhost:5000/categories/CATEGORY_ID/JSON](http://localhost:5000/categories/category_id/JSON) and [http://localhost:5000/item/ITEM_ID/JSON](http://localhost:5000/item/item_id/JSON) give access to the items of a single category and a single item, respectively.  

 


