//
//  Emotion.swift
//  Hoot
//
//  Created by Eric Luan on 2/27/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import Foundation
import UIKit

// Basic class to represent an emotions class and display it on the UI
class EmotionClass {
    var emotions: [Emotion]!
    var name: String!
    var backgroundColor: UIColor!
    
    init(backgroundColor: UIColor, name: String, emotions: [Emotion]) {
        self.backgroundColor = backgroundColor
        self.name = name
        self.emotions = emotions
    }
}

// Basic class to represent an emotion and display it on the UI
class Emotion {
    var color: UIColor!
    var name: String!
    
    init(color: UIColor, name: String) {
        self.color = color
        self.name = name
    }
}

struct Emotions {
    // Rage class 
    let rage = Emotion(color: UIColor.redColor(), name: "Rage")
    let anger = Emotion(color: UIColor.redColor().colorWithAlphaComponent(0.7), name: "Anger")
    let annoyance = Emotion(color: UIColor.redColor().colorWithAlphaComponent(0.4), name: "Annoyance")
    
    // Vigilance class 
    let vigilance = Emotion(color: UIColor.orangeColor(), name: "Vigiance")
    let anticipation = Emotion(color: UIColor.orangeColor().colorWithAlphaComponent(0.7), name: "Anticipation")
    let interest = Emotion(color: UIColor.orangeColor().colorWithAlphaComponent(0.4), name: "Interest")
    
    // Ecstasy class 
    let ecstasy = Emotion(color: UIColor.yellowColor(), name: "Ecstasy")
    let joy = Emotion(color: UIColor.yellowColor().colorWithAlphaComponent(0.7), name: "Joy")
    let security = Emotion(color: UIColor.yellowColor().colorWithAlphaComponent(0.4), name: "Security")
    
    // Admiration class 
    let admiration = Emotion(color: UIColor.greenColor(), name: "Admiration")
    let trust = Emotion(color: UIColor.greenColor().colorWithAlphaComponent(0.7), name: "Trust")
    let acceptance = Emotion(color: UIColor.greenColor().colorWithAlphaComponent(0.4), name: "Acceptance")
    
    // Loathing class 
    let loathing = Emotion(color: UIColor.init(red: 143.0/255.0, green: 0.0/255.0, blue: 255.0/255.0, alpha: 1.0), name: "Loathing")
    let disgust = Emotion(color: UIColor.init(red: 143.0/255.0, green: 0.0/255.0, blue: 255.0/255.0, alpha: 0.7), name: "Disgust")
    let boredom = Emotion(color: UIColor.init(red: 143.0/255.0, green: 0.0/255.0, blue: 255.0/255.0, alpha: 0.4), name: "Boredom")
    
    // Grief class 
    let grief = Emotion(color: UIColor.purpleColor(), name: "Grief")
    let sadness = Emotion(color: UIColor.purpleColor().colorWithAlphaComponent(0.7), name: "Sadness")
    let pensiveness = Emotion(color: UIColor.purpleColor().colorWithAlphaComponent(0.4), name: "Pensiveness")
    
    // Amazement class 
    let amazement = Emotion(color: UIColor.blueColor(), name: "Amazement")
    let surprise = Emotion(color: UIColor.blueColor().colorWithAlphaComponent(0.7), name: "Surprise")
    let distraction = Emotion(color: UIColor.blueColor().colorWithAlphaComponent(0.4), name: "Distraction")
    
    // Terror class 
    let terror = Emotion(color: UIColor.init(red: 0.0/255.0, green: 128.0/255.0, blue: 128.0/255.0, alpha: 1.0), name: "Terror")
    let fear = Emotion(color: UIColor.init(red: 0.0/255.0, green: 128.0/255.0, blue: 128.0/255.0, alpha: 0.7), name: "Fear")
    let apprehension = Emotion(color: UIColor.init(red: 0.0/255.0, green: 128.0/255.0, blue: 128.0/255.0, alpha: 0.4), name: "Apprehension")
}

struct EmotionClasses {
    let rageClass = EmotionClass(backgroundColor: UIColor.redColor(), name: "\u{1F620}", emotions: [Emotions().rage, Emotions().anger, Emotions().annoyance])
    let vigilanceClass = EmotionClass(backgroundColor: UIColor.orangeColor(), name: "\u{1F914}", emotions: [Emotions().vigilance, Emotions().anticipation, Emotions().interest])
    let ecstasyClass = EmotionClass(backgroundColor: UIColor.yellowColor(), name: "\u{1F604}", emotions: [Emotions().ecstasy, Emotions().joy, Emotions().security])
    let admirationClass = EmotionClass(backgroundColor: UIColor.greenColor(), name: "\u{1F60D}", emotions: [Emotions().admiration, Emotions().trust, Emotions().acceptance])
    let loathingClass = EmotionClass(backgroundColor: UIColor.init(red: 143.0/255.0, green: 0.0/255.0, blue: 255.0/255.0, alpha: 1.0),
        name: "\u{1F912}", emotions: [Emotions().loathing, Emotions().disgust, Emotions().boredom])
    let griefClass = EmotionClass(backgroundColor: UIColor.purpleColor(), name: "\u{1F62D}",
        emotions: [Emotions().grief, Emotions().sadness, Emotions().pensiveness])
    let amazementClass = EmotionClass(backgroundColor: UIColor.blueColor(), name: "\u{1F62E}",
        emotions: [Emotions().amazement, Emotions().surprise, Emotions().distraction])
    let terrorClass = EmotionClass(backgroundColor: UIColor.init(red: 0.0/255.0, green: 128.0/255.0, blue: 128.0/255.0, alpha: 1.0),
        name: "\u{1F628}", emotions: [Emotions().terror, Emotions().fear, Emotions().apprehension])
}
