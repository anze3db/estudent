package org.psywerx.estudent;


import java.util.ArrayList;
import java.util.List;

import org.psywerx.estudent.api.Api;
import org.psywerx.estudent.api.ResponseListener;
import org.psywerx.estudent.extra.D;
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
	private static String LINE_FORMAT = "%4s %6s %35s %7s %22s %12s %10s %15s";
	private ArrayList<String> groups = new ArrayList<String>();
	private ArrayList<ArrayList<String>> children = new ArrayList<ArrayList<String>>();
	private KartList mKartList;

	private int zaporedna = 1;

	private String head(){
		return "\n"+String.format(LINE_FORMAT, 
				"","Šifra", "Predmet", "KT/U", "Predavatelj(i)","Datum","Ocena", "Št. polaganj")+"\n";
	}

	private String split(String s,String sp,int w, boolean first){
		if (w < s.length()){
			int ind = s.substring(0, w).lastIndexOf(sp);
			if (first){
				return s.substring(0,Math.min(ind, s.length()));
			}else{
				return s.length() > ind ? s.substring(ind) : "";
			}
		}else{
			return first ? s:"";
		}
		
	}
	
	private String format(Index.SingleCourse course, Index.Polaganje polaganje){
		String result = "";
		String sifraPredmeta = "";
		String imePredmeta = "";
		String kreditneTocke = "";
		String predavatelj = "";
		String datum = "";
		String ocena = "";
		String polaganj = "";
		if (course != null){
			sifraPredmeta = course.sifra_predmeta;
			imePredmeta = course.name.replace("\n", "");
			kreditneTocke = ""+course.kreditne_tocke;
			predavatelj = course.predavatelj.replace("\n", "");
		}
		if (polaganje != null){
			datum = polaganje.datum;
			ocena = polaganje.ocena;
			polaganj = ""+polaganje.stevilo_polaganj;
		}
		
		result = String.format(LINE_FORMAT, 
				""+zaporedna++, sifraPredmeta,
				split(imePredmeta," ", 34, true),
				kreditneTocke+"",
				split(predavatelj,"/", 19, true),
				datum, ocena, polaganj);
		imePredmeta = split(imePredmeta," ", 34, false);
		predavatelj = split(predavatelj,"/", 19, false);
		int c = 0;
		while (c++<4 && (imePredmeta.length()>0 || predavatelj.length()>0)){
			
			result += "\n"+String.format(LINE_FORMAT, 
					"", "",
					split(imePredmeta," ", 34, true),
					"",
					split(predavatelj,"/", 19, true),
					"", "", "");
			imePredmeta = split(imePredmeta," ", 34, false);
			predavatelj = split(predavatelj,"/", 34, false);
		}
		D.dbgv(result);
		return result;
	}

	public MyExpandableListAdapter(KartList k,Index index) {
		super();
		mKartList = k;

		for(Index.Courses c: index.index) {
			groups.add(c.program);

			ArrayList<String> courses = new ArrayList<String>();
			courses.add(head());
			for (Index.SingleCourse course: c.courses){
				String courseFormat = "";
				if (course.polaganja.size()==0){
					courseFormat = (format(course, null));
					courses.add(courseFormat);
				}else{
					courseFormat = (format(course, course.polaganja.get(0)));
					courses.add(courseFormat);
					for (int i = 1; i < course.polaganja.size(); i++) {
						courseFormat = (format(null, course.polaganja.get(i)));
						courses.add(courseFormat);
					}
				}

			}

			children.add(courses);
		}
	}

	public View getChildView(int groupPosition, int childPosition, boolean isLastChild,
			View convertView, ViewGroup parent) {
		AbsListView.LayoutParams lp = new AbsListView.LayoutParams(
//				ViewGroup.LayoutParams.MATCH_PARENT, 32+20*(childPosition==0 ? 1 : 0));
				ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
		TextView textView = new TextView(mKartList);
		textView.setLayoutParams(lp);
		textView.setGravity(Gravity.CENTER_VERTICAL | Gravity.LEFT);
		textView.setPadding(36, 0, 0, 0);
		textView.setTypeface(Typeface.MONOSPACE);
		textView.setTextSize(16);
		if(childPosition == 0)
			textView.setBackgroundColor(Color.rgb(33, 66, 99));
		else if(childPosition % 2 == 0)
			textView.setBackgroundColor(Color.rgb(55, 55, 55));
		else
			textView.setBackgroundColor(Color.rgb(33, 33, 33));
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