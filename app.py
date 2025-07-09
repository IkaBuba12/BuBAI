from ext import app
from routes import index, login,register,load_user,logout,chat


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
