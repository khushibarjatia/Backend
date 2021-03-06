
import 'package:new_english/main.dart';
import 'package:flutter/material.dart';
import 'package:new_english/widgets/conceptcard.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'constants.dart';
class BasLinks{
  BasLinks(this.des, this.lin);
  String des;
  String lin;
}

class Lear extends StatefulWidget {
  
  @override
  _LearState createState() => _LearState();
}

class _LearState extends State<Lear> {
  List l=[];

  Future<List> getData()async{
    http.Response response=await http.get("https://626dcabefa3e.ngrok.io/basic"); 
   // print(response.body);
    Map jso =jsonDecode(response.body);
    //print(jso);
   setState(() {
     jso.entries.forEach((e) => l.add([e.key, e.value]));
   });
    return [jso];
  }
  
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
        /* Divider(),
         Padding(
           padding: const EdgeInsets.only(top:20.0,left:12.0),
           child: ListTile(title:Text("Premium"),leading: Image.asset("lib/images/crown.png"),onTap:(){
               Navigator.pushNamed(context,'/pre' );
           }, ),
         ),*/
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
        body: CustomScrollView(
            slivers: <Widget>[
               SliverAppBar(
               
                
                 backgroundColor: Colors.pinkAccent[100],
                expandedHeight: 150.0,
                floating: false,
                pinned: true,
                flexibleSpace: FlexibleSpaceBar(
                  centerTitle: true,
                  
                  title: Text("Basic",style: TextStyle(fontFamily:"Daddy",fontSize: 33.3),),
                ),
              ),

              

              FutureBuilder(

                 future: getData(),
                 builder: (context,snapshot){
                   if(snapshot.data==null){
                     return SliverList(
                  delegate: SliverChildListDelegate([
                   SizedBox(
                      height: 200.0,
                      width: 200.0,
                       child: spinkit
                   )
                   ],
                  ),
                  
                  );
                   }
                   else{
                     return SliverList(
                  
                  delegate:SliverChildBuilderDelegate(
                    
                    (BuildContext context,int index){
                      
                       return ConceptCard(l: l[index],);
                       
                       },
                       childCount: 4
                       
                  )
                  );
                   }
                 }
                    
                    
                    /* SliverList(
                  
                  delegate:SliverChildBuilderDelegate(
                    (BuildContext context,int index){
                     return ConceptCard(l: l[index],);
                    }
                  )
              ),*/
               ),
            ],
        ),
      ),
          ),
    );
  }
} 