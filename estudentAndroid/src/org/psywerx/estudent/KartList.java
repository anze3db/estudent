package org.psywerx.estudent;
import android.app.ExpandableListActivity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.BaseExpandableListAdapter;
import android.widget.ExpandableListAdapter;
import android.widget.TextView;


public class KartList extends ExpandableListActivity{
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		ExpandableListAdapter mAdapter = new MyExpandableListAdapter();
		setListAdapter(mAdapter);
	}
	
    public class MyExpandableListAdapter extends BaseExpandableListAdapter {
        // Sample data set.  children[i] contains the children (String[]) for groups[i].
        private String[] groups = { "People Names", "Dog\n\tNames", "Cat Names", "Fish Names" };
        private String[][] children = {
                { "Arnold", "Barry", "Chuck", "David" },
                { "Ace", "Bandit", "Cha-Cha", "Deuce" },
                { "Fluffy", "Snuggles" },
                { "Goldy", "Bubbles" }
        };
        
        public View getChildView(int groupPosition, int childPosition, boolean isLastChild,
                View convertView, ViewGroup parent) {
        	AbsListView.LayoutParams lp = new AbsListView.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, 32+20*(childPosition==0 ? 1 : 0));
        	TextView textView = new TextView(KartList.this);
        	textView.setLayoutParams(lp);
        	textView.setGravity(Gravity.CENTER_VERTICAL | Gravity.LEFT);
        	textView.setPadding(36, 0, 0, 0);
        	
            if(childPosition == 0)
            	textView.setBackgroundColor(Color.GRAY);
            else if(childPosition % 2 == 0)
            	textView.setBackgroundColor(Color.BLUE);
            else
            	textView.setBackgroundColor(Color.CYAN);
            textView.setText(getChild(groupPosition, childPosition).toString());
            return textView;
        }
        
        public View getGroupView(int groupPosition, boolean isExpanded, View convertView,
                ViewGroup parent) {
        	AbsListView.LayoutParams lp = new AbsListView.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT, 64);
        	TextView textView = new TextView(KartList.this);
        	textView.setLayoutParams(lp);
        	textView.setGravity(Gravity.CENTER_VERTICAL | Gravity.LEFT);
        	textView.setPadding(64, 0, 0, 0);
            textView.setText(getGroup(groupPosition).toString());
            return textView;
        }

        public Object getChild(int groupPosition, int childPosition) {
            return children[groupPosition][childPosition];
        }

        public long getChildId(int groupPosition, int childPosition) {
            return childPosition;
        }

        public int getChildrenCount(int groupPosition) {
            return children[groupPosition].length;
        }

        public Object getGroup(int groupPosition) {
            return groups[groupPosition];
        }

        public int getGroupCount() {
            return groups.length;
        }

        public long getGroupId(int groupPosition) {
            return groupPosition;
        }

        public boolean isChildSelectable(int groupPosition, int childPosition) {
            return false;
        }

        public boolean hasStableIds() {
            return true;
        }

    }
}

