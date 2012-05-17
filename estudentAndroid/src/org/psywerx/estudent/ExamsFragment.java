package org.psywerx.estudent;

import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.app.ListFragment;
import android.content.Context;
import android.os.Bundle;
import android.view.View;
import android.widget.ListView;

public class ExamsFragment extends ListFragment {
	
	private Context mContext;
	
	private MenuAdapter mMenuAdapter;
	private OnExamSelectedListener mExamSelectedListener;
	
	public interface OnExamSelectedListener {
		public void onExamSelected(int action);
	}
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		mContext = getActivity().getApplicationContext();
		
		List<MenuItem> aaa = new ArrayList<MenuItem>();
		aaa.add(new MenuItem("aaa", "neki", 0));
		aaa.add(new MenuItem("bbb", "neki1", 1));
		
		mMenuAdapter = new MenuAdapter(mContext, aaa);
		setListAdapter(mMenuAdapter);
	}
	
	@Override
	public void onAttach(Activity activity) {
		super.onAttach(activity);
		mExamSelectedListener = (OnExamSelectedListener) activity;
	}
	
	@Override
	public void onListItemClick(ListView l, View v, int position, long id) {
		super.onListItemClick(l, v, position, id);
		
		mExamSelectedListener.onExamSelected(mMenuAdapter.getItem(position).getAction());
	}

}
