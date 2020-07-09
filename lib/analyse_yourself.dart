import 'package:flutter/material.dart';
import './quiz1.dart';
import './quiz2.dart'; 



class Quiz extends StatefulWidget{
  @override 
  State<StatefulWidget> createState() {
   return new QuizState();
  }
}

class QuizState extends State<Quiz>{
  @override
  Widget build(BuildContext context) {
   return new Scaffold(
     appBar: new AppBar(
       title: new Text("Analyse Yourself"),
       backgroundColor: Colors.blue[900], 
     ),


     body: new Container(
          margin: const EdgeInsets.all(50.0),
       child: new Column(
          
         crossAxisAlignment: CrossAxisAlignment.stretch,
         mainAxisAlignment: MainAxisAlignment.center,
         children: <Widget>[

           new MaterialButton(
             height: 40.0, 
               color: Colors.green,
               onPressed: startQuiz1,
               child: new Text("Test your Grammar",
                 style: new TextStyle(
                     fontSize: 18.0,
                     color: Colors.white
                 ),)
                
           ),

           new MaterialButton(
             height: 40.0,
               color: Colors.green,
               onPressed: startQuiz2, 
               child: new Text("Test your Vocabulary",
                 style: new TextStyle(
                     fontSize: 18.0,
                     color: Colors.white
                 ),)
                
           ),


         ],
       ),
     ),
     


   );
  }

  void startQuiz1(){
   setState(() {
     Navigator.push(context, new MaterialPageRoute(builder: (context)=> new Quiz1()));
   });
  }

  void startQuiz2(){
   setState(() {
     Navigator.push(context, new MaterialPageRoute(builder: (context)=> new Quiz2())); 
   });
  }


}
