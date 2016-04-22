//
//  ViewController.swift
//  Hoot
//
//  Created by Eric Luan on 2/27/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UITableViewDataSource, UITableViewDelegate, UISearchBarDelegate {
    

    @IBOutlet weak var activityIndicator: UIActivityIndicatorView!
    @IBOutlet weak var searchSuggestionsTable: UITableView!
    @IBOutlet weak var searchBar: UISearchBar!
    @IBOutlet weak var navBar: UINavigationItem!
    
    let hootAPI: HootAPI = HootAPI() // Class used to get data from the HOOT API
    
    // Used for the search bar header
    var emotionCategories: [String]!
    var admirationCategory: [String]!
    var amazementCategory: [String]!
    var ecstasyCategory: [String]!
    var griefCategory: [String]!
    var loathingCategory: [String]!
    var rageCategory: [String]!
    var terrorCategory: [String]!
    
    var vigilanceCategory: [String]!
    var selectedControl: [String]!
    
    var suggestions: [Product] = TestData.getTestData()
    var category: String = ""
    var selectedRow: Int?
    
    override func viewDidLoad() {
        searchSuggestionsTable.delegate = self
        searchSuggestionsTable.dataSource = self
        searchBar.delegate = self
        searchSuggestionsTable.hidden = true // TODO: Set this to false when we are ready to deploy
        suggestions = hootAPI.getSuggestions(nil, emotionText: nil)
        
        emotionCategories = [
            EmotionClasses().admirationClass.name,
            EmotionClasses().amazementClass.name,
            EmotionClasses().ecstasyClass.name,
            EmotionClasses().griefClass.name,
            EmotionClasses().loathingClass.name,
            EmotionClasses().rageClass.name,
            EmotionClasses().terrorClass.name,
            EmotionClasses().vigilanceClass.name]
        
        admirationCategory = [
            "Back",
            "Admiration",
            "Trust",
            "Acceptance"]
        
        amazementCategory = [
            "Back",
            "Amazement",
            "Surprise",
            "Distraction"]
        
        ecstasyCategory = [
            "Back",
            "Ecstasy",
            "Joy",
            "Security"]
        
        griefCategory = [
            "Back",
            "Grief",
            "Sadness",
            "Pensiveness"]
        
        loathingCategory = [
            "Back",
            "Loathing",
            "Disgust",
            "Boredom"]
        
        rageCategory = [
            "Back",
            "Rage",
            "Anger",
            "Annoyance"]
        
        terrorCategory = [
            "Back",
            "Terror",
            "Fear",
            "Apprehension"]
        
        vigilanceCategory = [
            "Back",
            "Vigilance",
            "Anticipation",
            "Interest"]
        
        selectedControl = emotionCategories
        searchBar.scopeButtonTitles = emotionCategories
        searchBar.showsScopeBar = false
        searchBar.selectedScopeButtonIndex = -1
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
    }
    
    func searchBarCancelButtonClicked(searchBar: UISearchBar) {
        searchBar.resignFirstResponder()
    }
    
    func searchBarSearchButtonClicked(searchBar: UISearchBar) {
        searchBar.resignFirstResponder()
        var query: String? = nil
        var emotion: String? = nil
        let searchText = searchBar.text
        if category != "" {
            emotion = category
        }
        
        if searchText != "" {
            query = searchText
        }
        activityIndicator.startAnimating()
        hootAPI.getRealSuggestions(query, emotionText: emotion, completionHandler: {data, error -> Void in
            self.suggestions = data
            self.searchSuggestionsTable.reloadData()
            self.activityIndicator.stopAnimating()
        })
    }
    
    func searchBarShouldBeginEditing(searchBar: UISearchBar) -> Bool {
        searchBar.showsScopeBar = true
        return true
    }
    
    func searchBarShouldEndEditing(searchBar: UISearchBar) -> Bool {
        searchBar.showsScopeBar = false
        return true
    }
    
    func searchBar(searchBar: UISearchBar, selectedScopeButtonIndexDidChange selectedScope: Int) {
        if emotionCategories == searchBar.scopeButtonTitles! {
            changeSearchScope(selectedScope)
            category = ""
        } else if (selectedScope == 0) {
            searchBar.scopeButtonTitles = emotionCategories
            searchBar.selectedScopeButtonIndex = -1
            selectedControl = emotionCategories
            category = ""
        } else {
            category = selectedControl[selectedScope]
            print(category)
        }
    }
    
    func searchBar(searchBar: UISearchBar, textDidChange searchText: String) {

    }
    
    func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return suggestions.count
    }
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        let cell = searchSuggestionsTable.dequeueReusableCellWithIdentifier("Cell")! as! SearchResultTableCell;
        cell.product = suggestions[indexPath.row]
        cell.setValues()
        // TODO: Implement product view stuff 
        return cell
    }
    
    func changeSearchScope(index: Int) {
        let selectedTitle: String = selectedControl[index]
        switch selectedTitle {
        case EmotionClasses().rageClass.name:
            selectedControl = rageCategory
            searchBar.scopeButtonTitles = rageCategory
        case EmotionClasses().loathingClass.name:
            selectedControl = loathingCategory
            searchBar.scopeButtonTitles = loathingCategory
        case EmotionClasses().griefClass.name:
            selectedControl = griefCategory
            searchBar.scopeButtonTitles = griefCategory
        case EmotionClasses().ecstasyClass.name:
            selectedControl = ecstasyCategory
            searchBar.scopeButtonTitles = ecstasyCategory
        case EmotionClasses().admirationClass.name:
            selectedControl = admirationCategory
            searchBar.scopeButtonTitles = admirationCategory
        case EmotionClasses().amazementClass.name:
            selectedControl = amazementCategory
            searchBar.scopeButtonTitles = amazementCategory
        case EmotionClasses().terrorClass.name:
            selectedControl = terrorCategory
            searchBar.scopeButtonTitles = terrorCategory
        case EmotionClasses().vigilanceClass.name:
            selectedControl = vigilanceCategory
            searchBar.scopeButtonTitles = vigilanceCategory
        default:
            break
        }
        searchBar.selectedScopeButtonIndex = -1
        self.searchSuggestionsTable.reloadData()
    }

    func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        selectedRow = indexPath.row
        performSegueWithIdentifier("GoToProductPage", sender: self)
    }
    
    override func shouldPerformSegueWithIdentifier(identifier: String, sender: AnyObject?) -> Bool {
        return selectedRow != nil
    }
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "GoToProductPage" {
            if let destination = segue.destinationViewController as? ProductViewController {
                
                guard let row = selectedRow where selectedRow != nil else {
                    return
                }
                let product: Product = suggestions[row]
                destination.product = product.name
                destination.comments = product.comments
                destination.emotionText = product.emotions
                destination.summaryText = product.description
                let cell = searchSuggestionsTable.cellForRowAtIndexPath(NSIndexPath(forRow: row, inSection: 0)) as! SearchResultTableCell
                destination.productImage = cell.thumbnail.image
                
                
            }
        }
    }
    
}

