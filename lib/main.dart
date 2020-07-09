import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:new_english/analyse_yourself.dart';
import 'package:new_english/basic.dart';
import 'package:new_english/advanced.dart';
import 'package:new_english/home.dart';
import 'package:new_english/texttospeech.dart';
import 'package:new_english/widgets/provider_widget.dart'; 
import 'package:new_english/services/auth_service.dart';
import 'package:new_english/views/first_view.dart';
import 'package:new_english/views/sign_up_view.dart'; 
import 'package:new_english/dictionary.dart';
import 'package:new_english/books.dart';  
import 'package:new_english/quiz1.dart';

void main(){
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Provider( 
      auth: AuthService(),
      child: MaterialApp(
        title: "English App",
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        debugShowCheckedModeBanner: false,
        home: HomeController(), 
        routes: <String, WidgetBuilder>{
          '/signUp': (BuildContext context) => SignUpView(authFormType: AuthFormType.signUp),
          '/signIn': (BuildContext context) => SignUpView(authFormType: AuthFormType.signIn), 
          '/home': (BuildContext context) => HomeController(),
          '/dic': (context) => Dic(), 
          '/bk': (context) => BookApp(), 
          '/textToSpeech': (context) => Texttospeech(), 
          '/basic': (context) => Lear(),
          '/advanced': (context) => Adv(),
          '/an': (context) => Quiz(),
        }, 
      ), 
      
    );
  } 
}

class HomeController extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final AuthService auth = Provider.of(context).auth;
    return StreamBuilder(
      stream: auth.onAuthStateChanged,
      builder: (context, AsyncSnapshot<String> snapshot){
        if(snapshot.connectionState == ConnectionState.active){
          final bool signedIn = snapshot.hasData;
          return signedIn ? LevelPage() : FirstView(); 
        }
        return CircularProgressIndicator(); 

      },
    );
  }
}




                  