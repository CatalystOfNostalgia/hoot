//
//  ReviewsViewController.swift
//  Hoot
//
//  Created by Eric Luan on 4/12/16.
//  Copyright © 2016 Eric Luan. All rights reserved.
//

import UIKit

class ReviewsViewController: UITableViewController {
    
    var comments: [Comment]?
    var selectedComment: Comment?
    
    // MARK: UITableViewController
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {
        
        let cell = self.tableView.dequeueReusableCellWithIdentifier("Cell") as! ReviewTableCell
        let index = indexPath.row
        
        cell.relevancyLabel.text = "Relevancy: \(comments![index].relevancy)"
        cell.reviewTextPreview.text = comments![index].comment
        cell.reviewTextPreview.setContentOffset(CGPointZero, animated: false)
        
        return cell
    }
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return (comments?.count)!
    }
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        selectedComment = comments![indexPath.row]
        performSegueWithIdentifier("GoToCommentSpecifics", sender: self)
    }
    
    // MARK: Navigation
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        if segue.identifier == "GoToCommentSpecifics" {
            if let rvc = segue.destinationViewController as? ReviewViewController {
                rvc.comment = selectedComment!
            }
        }
    }
}
