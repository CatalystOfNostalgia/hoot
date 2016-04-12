//
//  ViewController.swift
//  Hoot
//
//  Created by Eric Luan on 2/27/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, UISearchBarDelegate {
    

    @IBOutlet weak var searchSuggestionsTable: UITableView!
    @IBOutlet weak var searchBar: UISearchBar!
    @IBOutlet weak var navBar: UINavigationItem!
    
    let hootAPI: HootAPI = HootAPI() // Class used to get data from the HOOT API
    
    // Used for the search bar header
    var emotionCategories: UISegmentedControl!
    var admirationCategory: UISegmentedControl!
    var amazementCategory: UISegmentedControl!
    var ecstasyCategory: UISegmentedControl!
    var griefCategory: UISegmentedControl!
    var loathingCategory: UISegmentedControl!
    var rageCategory: UISegmentedControl!
    var terrorCategory: UISegmentedControl!
    var vigilanceCategory: UISegmentedControl!
    var selectedControl: UISegmentedControl!
    
    var suggestions: [String] = []
    var category: String = ""
    
    override func viewDidLoad() {
        searchSuggestionsTable.delegate = self
        searchSuggestionsTable.dataSource = self
        searchBar.delegate = self
        searchSuggestionsTable.hidden = true
        suggestions = hootAPI.getInitialSuggestions()
        
        emotionCategories = UISegmentedControl(items: [
            EmotionClasses().admirationClass.name,
            EmotionClasses().amazementClass.name,
            EmotionClasses().ecstasyClass.name,
            EmotionClasses().griefClass.name,
            EmotionClasses().loathingClass.name,
            EmotionClasses().rageClass.name,
            EmotionClasses().terrorClass.name,
            EmotionClasses().vigilanceClass.name])
        
        emotionCategories.addTarget(self, action: #selector(ViewController.categoryValueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        admirationCategory = UISegmentedControl(items: [
            "Back",
            "Admiration",
            "Trust",
            "Acceptance"])

        admirationCategory.addTarget(self, action: #selector(ViewController.valueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        amazementCategory = UISegmentedControl(items: [
            "Back",
            "Amazement",
            "Surprise",
            "Distraction"])
        
        amazementCategory.addTarget(self, action: #selector(ViewController.valueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        ecstasyCategory = UISegmentedControl(items: [
            "Back",
            "Ecstasy",
            "Joy",
            "Security"])
        
        ecstasyCategory.addTarget(self, action: #selector(ViewController.valueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        griefCategory = UISegmentedControl(items: [
            "Back",
            "Grief",
            "Sadness",
            "Pensiveness"])
        
        griefCategory.addTarget(self, action: #selector(ViewController.valueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        loathingCategory = UISegmentedControl(items: [
            "Back",
            "Loathing",
            "Disgust",
            "Boredom"])
        
        loathingCategory.addTarget(self, action: #selector(ViewController.valueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        rageCategory = UISegmentedControl(items: [
            "Back",
            "Rage",
            "Anger",
            "Annoyance"])
        
        rageCategory.addTarget(self, action: #selector(ViewController.valueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        terrorCategory = UISegmentedControl(items: [
            "Back",
            "Terror",
            "Fear",
            "Apprehension"])
        
        terrorCategory.addTarget(self, action: #selector(ViewController.valueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        vigilanceCategory = UISegmentedControl(items: [
            "Back",
            "Vigilance",
            "Anticipation",
            "Interest"])
        
        vigilanceCategory.addTarget(self, action: #selector(ViewController.valueChanged(_:)), forControlEvents: UIControlEvents.ValueChanged)
        
        selectedControl = emotionCategories
        navBar.title = "Hoot"
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func searchBarTextDidBeginEditing(searchBar: UISearchBar) {
        searchSuggestionsTable.hidden = false
    }
    
    func searchBarTextDidEndEditing(searchBar: UISearchBar) {
        searchBar.resignFirstResponder()
        searchSuggestionsTable.hidden = true
    }
    
    func searchBarCancelButtonClicked(searchBar: UISearchBar) {
        searchBar.resignFirstResponder()
        searchSuggestionsTable.hidden = true
    }
    
    func searchBarSearchButtonClicked(searchBar: UISearchBar) {
        searchBar.resignFirstResponder()
        searchSuggestionsTable.hidden = true
    }
    
    func searchBar(searchBar: UISearchBar, textDidChange searchText: String) {
        
        if searchText == "" {
            suggestions = hootAPI.getInitialSuggestions() // Display some default goodness
        } else {
            suggestions = hootAPI.getSuggestions(searchText) // Otherwise try to do useful things
        }
        
        self.searchSuggestionsTable.reloadData()
    }
    
    func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
        return 44.0
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return suggestions.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = searchSuggestionsTable.dequeueReusableCellWithIdentifier("Cell")! as! SearchResultTableCell;
        // TODO: Implement product view stuff 
        return cell
    }
    
    func tableView(tableView: UITableView, viewForHeaderInSection section: Int) -> UIView? {
        if section == 0 {
            return selectedControl
        } else {
            return nil
        }
    }
    
    func categoryValueChanged(segmentedControl: UISegmentedControl) {
        let selectedTitle: String = segmentedControl.titleForSegmentAtIndex(segmentedControl.selectedSegmentIndex)!
        
        switch selectedTitle {
        case EmotionClasses().rageClass.name:
            selectedControl = rageCategory
        case EmotionClasses().loathingClass.name:
            selectedControl = loathingCategory
        case EmotionClasses().griefClass.name:
            selectedControl = griefCategory
        case EmotionClasses().ecstasyClass.name:
            selectedControl = ecstasyCategory
        case EmotionClasses().admirationClass.name:
            selectedControl = admirationCategory
        case EmotionClasses().amazementClass.name:
            selectedControl = amazementCategory
        case EmotionClasses().terrorClass.name:
            selectedControl = terrorCategory
        case EmotionClasses().vigilanceClass.name:
            selectedControl = vigilanceCategory
        default:
            break
        }
        
        self.searchSuggestionsTable.reloadData()
    }
    
    func valueChanged(segmentedControl: UISegmentedControl) {
        let selectedTitle: String = segmentedControl.titleForSegmentAtIndex(segmentedControl.selectedSegmentIndex)!
        
        if selectedTitle == "Back" {
            category = ""
            selectedControl.selectedSegmentIndex = -1
            selectedControl = emotionCategories
            selectedControl.selectedSegmentIndex = -1
        } else {
            category = selectedTitle
        }
        
        self.searchSuggestionsTable.reloadData()
    }
    
}

