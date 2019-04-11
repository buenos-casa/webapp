Dependencies:

If you haven't already, install nodejs on your machine.

Once that is finished enter the webapp directory and run 'npm install'. (This will take some time)

While this is happening, install python 3 if not already installed.

Again go to the webapp directory but this time run 'pip install -r requirements.txt'

Development environment:

To build the webapp, run 'npm run build'. However you would need to do this every time you want to see changes. If you want live updates, run 'npm run watch'.

To run the server, run the command 'python run.py'.

Use a browser to go to localhost:8080 and see your changes.

If just getting started with VueJS I suggest looking at the Single File Components already in the project and see how they are structured and how they are imported into the app proper in script.js.

** Important, to import your SFC the variable name must be the name of the file such that "buenosaires" is imported as Buenosaires. If you do not do it this way, the component will not be imported.
