package org.psywerx.estudent;


import java.util.ArrayList;

import org.psywerx.estudent.api.Api;
import org.psywerx.estudent.api.ResponseListener;
import org.psywerx.estudent.json.Index;

import android.app.ExpandableListActivity;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.BaseExpandableListAdapter;
import android.widget.ExpandableListAdapter;
import android.widget.ExpandableListView;
import android.widget.ExpandableListView.OnGroupClickListener;
import android.widget.TextView;


public class KartList extends ExpandableListActivity implements ResponseListener{

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		Api.getIndex(this, StaticData.username);

	}


	@Override
	public void onServerResponse(Object o) {
		if (o != null && o instanceof Index){
			ExpandableListAdapter mAdapter = new MyExpandableListAdapter(this,(Index)o);
			setListAdapter(mAdapter);
			Bundle extras = getIntent().getExtras();
			if(extras.getBoolean("expand")) {
				for(int i = 0; i < mAdapter.getGroupCount(); i++)
					getExpandableListView().expandGroup(i);
				getExpandableListView().setOnGroupClickListener(new OnGroupClickListener() {
					public boolean onGroupClick(ExpandableListView parent, View v, int groupPosition, long id) {
						return true;
					}
				});
			}

		}else {
			finish();
		}
	}
}


class MyExpandableListAdapter extends BaseExpandableListAdapter {
	private static String LINE_FORMAT = "%4s %8s %30s %7s %26s %14s %10s %15s";
	private ArrayList<String> groups = new ArrayList<String>();
	private ArrayList<ArrayList<String>> children = new ArrayList<ArrayList<String>>();
	private KartList mKartList;

	private int zaporedna = 1;

	private String head(){
		return String.format(LINE_FORMAT, 
				"","Šifra", "Predmet", "KT/U", "Predavatelj(i)","Datum","Ocena", "Št. polaganj");
	}

	private String format(Index.SingleCourse course, Index.Polaganje polaganje){
		String sifraPredmeta = "";
		String imePredmeta = "";
		String kreditneTocke = "";
		String predavatelj = "";
		String datum = "";
		String ocena = "";
		String polaganj = "";
		if (course != null){
			sifraPredmeta = course.sifra_predmeta;
			imePredmeta = course.name;
			kreditneTocke = ""+course.kreditne_tocke;
			predavatelj = course.predavatelj;
		}
		if (polaganje != null){
			datum = polaganje.datum;
			ocena = polaganje.ocena;
			polaganj = ""+polaganje.stevilo_polaganj;
		}

		return String.format(LINE_FORMAT, 
				""+zaporedna++, sifraPredmeta, imePredmeta, kreditneTocke+" ",
				predavatelj, datum, ocena, polaganj);


	}

	public MyExpandableListAdapter(KartList k,Index index) {
		super();
		mKartList = k;

		for(Index.Courses c: index.index) {
			groups.add(c.program);

			ArrayList<String> courses = new ArrayList<String>();
			courses.add(head());
			for (Index.SingleCourse course: c.courses){
				if (course.polaganja.size()==0){
					courses.add(format(course, null));
				}else{
					courses.add(format(course, course.polaganja.get(0)));
					for (int i = 1; i < course.polaganja.size(); i++) {
						courses.add(format(null, course.polaganja.get(i)));
					}
				}

			}

			children.add(courses);
		}
	}

	public View getChildView(int groupPosition, int childPosition, boolean isLastChild,
			View convertView, ViewGroup parent) {
		AbsListView.LayoutParams lp = new AbsListView.LayoutParams(
				ViewGroup.LayoutParams.MATCH_PARENT, 32+20*(childPosition==0 ? 1 : 0));
		TextView textView = new TextView(mKartList);
		textView.setLayoutParams(lp);
		textView.setGravity(Gravity.CENTER_VERTICAL | Gravity.LEFT);
		textView.setPadding(36, 0, 0, 0);
		textView.setTypeface(Typeface.MONOSPACE);
		textView.setTextSize(16);
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
		TextView textView = new TextView(mKartList);
		textView.setLayoutParams(lp);
		textView.setGravity(Gravity.CENTER_VERTICAL | Gravity.LEFT);
		textView.setPadding(64, 0, 0, 0);
		textView.setText(getGroup(groupPosition).toString());
		return textView;
	}

	public Object getChild(int groupPosition, int childPosition) {
		return children.get(groupPosition).get(childPosition);
	}

	public long getChildId(int groupPosition, int childPosition) {
		return childPosition;
	}

	public int getChildrenCount(int groupPosition) {
		return children.get(groupPosition).size();
	}

	public Object getGroup(int groupPosition) {
		return groups.get(groupPosition);
	}

	public int getGroupCount() {
		return groups.size();
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
