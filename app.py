from ext import app
from routes import index, login,register,load_user,logout,chat


app.run(debug=True, host='0.0.0.0')
