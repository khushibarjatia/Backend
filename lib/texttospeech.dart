import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart'; 


class Texttospeech extends StatelessWidget {
  final FlutterTts flutterTts = FlutterTts();
  
  @override
  Widget build(BuildContext context) {

    TextEditingController textEditingController = TextEditingController(); 

    Future _speak(String text) async {
      await flutterTts.setLanguage("en-US"); 
      await flutterTts.setPitch(1); 
      await flutterTts.speak(text); 
    }
    return new Scaffold(
      body: Container(
        alignment: Alignment.center,
        child: Column(

          mainAxisSize: MainAxisSize.min,
          children: <Widget>[ 
            TextFormField(
              controller: textEditingController, 
            ),
            RaisedButton(
              child: Text("Tap this"),
              onPressed: () => _speak(textEditingController.text),  
            )
          ],
        ) 
      )     
    );
  }
}