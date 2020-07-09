//import 'package:commitment/widgets/result.dart';
import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart'; 
import 'package:new_english/LevelButton.dart';
import 'package:new_english/services/auth_service.dart';
import 'package:new_english/widgets/provider_widget.dart'; 
import 'dart:convert';


class LevelPage extends StatefulWidget {
  @override
  _LevelPageState createState() => _LevelPageState();
}

class _LevelPageState extends State<LevelPage> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: SafeArea(
        child: Scaffold(
          drawer: Drawer(             
            child:ListView(children: <Widget>[
              //DrawerHeader(child: Text("Hello, $user")),
              Padding(
                padding: const EdgeInsets.only(top:20.0,left:12.0),
                child: ListTile(title:Center(child: Text("Features",style: TextStyle(fontSize:25.0),))),
              ),
              Divider(),
              Padding(
                padding: const EdgeInsets.only(top:20.0,left:12.0),
                child: ListTile(title:Text("Novels"),leading: Image.asset("lib/images/Books.png"),onTap: (){
                  Navigator.pushNamed(context, '/bk');
                },),
              ),
              Divider(), 
              Padding(
                padding: const EdgeInsets.only(top:20.0,left:12.0),
                child: ListTile(title:Text("Dictionary"),leading: Image.asset("lib/images/Dictionary.png"),onTap: (){
                  Navigator.pushNamed(context, '/dic');
                },),
              ),
              Divider(),
              Padding(
                padding: const EdgeInsets.only(top:20.0,left:7.6),
                child: ListTile(title:Text("Analyse Yourself"),leading: Image.asset("lib/images/analyse.png"),onTap:(){
                  Navigator.pushNamed(context, '/an');
                } ),
              ),
              Divider(),
              Padding(
                padding: const EdgeInsets.only(top:20.0,left:12.0),
                child: ListTile(title:Text("Grammar Books"),leading: Image.asset("lib/images/pdf.png"),onTap:(){
                  Navigator.pushNamed(context, '/pdf');
                }, ),
              ),
              Divider(),
              Padding(
                padding: const EdgeInsets.only(top:20.0,left:12.0),
                child: ListTile(title:Text("Basic Courses"),leading: Image.asset("lib/images/basic.png"),onTap:(){
                  Navigator.pushNamed(context, '/basic'); 
                }, ),
              ),
              Divider(),
              Padding(
                padding: const EdgeInsets.only(top:20.0,left:12.0),
                child: ListTile(title:Text("Advanced Courses"),leading: Image.asset("lib/images/advanced.png"),onTap:(){
                  Navigator.pushNamed(context, '/advanced'); 
                }, ),
              ),
              Divider(),
              Padding(
                padding: const EdgeInsets.only(top:20.0,left:12.0),
                child: ListTile(title:Text("Pronounciation"),leading: Image.asset("lib/images/texttospeech.png"),onTap:(){
                  Navigator.pushNamed(context, '/textToSpeech'); 
                }, ),
              ),
            ],)
          ),
          
          backgroundColor: Colors.white,
          appBar: AppBar(
            backgroundColor: Colors.lightBlue[900],
            title: Text("Hi!"),
            actions: <Widget>[
              IconButton(
                icon: Icon(Icons.undo),
                onPressed: () async {
                  try {
                    AuthService auth = Provider.of(context).auth;
                    await auth.signOut();
                    print("Signed Out");
                  } catch (e) {
                    print(e);
                  }
                },
              )
            ],
          ),

        ),
      ),
    );
  }
}
    
  
