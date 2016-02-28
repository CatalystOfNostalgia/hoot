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
    
    let hootAPI: HootAPI = HootAPI() // Class used to get data from the HOOT API
    var emotionCategories: UISegmentedControl!
    var suggestions: [String] = []
    
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
            suggestions = hootAPI.getInitialSuggestions()
        } else {
            suggestions = hootAPI.getSuggestions(searchText)
        }
        
        self.searchSuggestionsTable.reloadData()
    }
    
    func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return suggestions.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = searchSuggestionsTable.dequeueReusableCellWithIdentifier("Cell")! as UITableViewCell;
        cell.textLabel?.text = suggestions[indexPath.row]
        return cell
    }
}

