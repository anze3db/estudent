package org.psywerx.estudent;

import java.util.ArrayList;

import android.app.ListActivity;
import android.app.ProgressDialog;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.ContextMenu;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.ContextMenu.ContextMenuInfo;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import android.widget.Toast;

public class AppliedExamsActivity extends ListActivity {

	private ProgressDialog mProgressDialog = null;
	private ArrayList<MenuItem> mOrders = null;
	private OrderAdapter mAdapter;
	private Runnable mViewOrders;
	
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.menu_layout);
		mOrders = new ArrayList<MenuItem>();
		this.mAdapter = new OrderAdapter(this, R.layout.exams_row, mOrders);
		setListAdapter(this.mAdapter);
		
		registerForContextMenu(getListView());

		mViewOrders = new Runnable(){
			public void run() {
				getExamsList();
			}
		};
		Thread thread =  new Thread(null, mViewOrders, "MagentoBackground");
		thread.start();
		mProgressDialog = ProgressDialog.show(AppliedExamsActivity.this,    
				"Please wait...", "Retrieving data ...", true);
	}
	
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v,
			ContextMenuInfo menuInfo) {
		super.onCreateContextMenu(menu, v, menuInfo);
		menu.add(R.string.unapply);
	}
	
	@Override
	public boolean onContextItemSelected(android.view.MenuItem item) {
		AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo)item.getMenuInfo();
		Toast.makeText(this, "Odjava od izpita "+info.position, Toast.LENGTH_SHORT).show();  
		return super.onContextItemSelected(item);
	}
	
	private Runnable returnRes = new Runnable() {
		public void run() {
			if(mOrders != null && mOrders.size() > 0){
				mAdapter.notifyDataSetChanged();
				for(int i=0;i<mOrders.size();i++)
					mAdapter.add(mOrders.get(i));
			}
			mProgressDialog.dismiss();
			mAdapter.notifyDataSetChanged();
		}
	};
	
	private void getExamsList(){		
		try{
			mOrders = new ArrayList<MenuItem>();
			MenuItem o1 = new MenuItem();
			o1.setItemName("SF services");
			o1.setItemDescription("Pending");
			MenuItem o2 = new MenuItem();
			o2.setItemName("SF Advertisement");
			o2.setItemDescription("Completed");
			mOrders.add(o1);
			mOrders.add(o2);
			Thread.sleep(1500);
			Log.i("ARRAY", ""+ mOrders.size());
		} catch (Exception e) {
			Log.e("BACKGROUND_PROC", e.getMessage());
		}
		runOnUiThread(returnRes);
	}
	
	private class OrderAdapter extends ArrayAdapter<MenuItem> {

		private ArrayList<MenuItem> items;

		public OrderAdapter(Context context, int textViewResourceId, ArrayList<MenuItem> items) {
			super(context, textViewResourceId, items);
			this.items = items;
		}
		@Override
		public View getView(int position, View convertView, ViewGroup parent) {
			View v = convertView;
			if (v == null) {
				LayoutInflater vi = (LayoutInflater)getSystemService(Context.LAYOUT_INFLATER_SERVICE);
				v = vi.inflate(R.layout.exams_row, null);
			}
			MenuItem o = items.get(position);
			if (o != null) {
				TextView tt = (TextView) v.findViewById(R.id.toptext);
				TextView bt = (TextView) v.findViewById(R.id.bottomtext);
				if (tt != null) {
					tt.setText("Name: "+o.getItemName());                            }
				if(bt != null){
					bt.setText("Status: "+ o.getItemDescription());
				}
			}
			return v;
		}
	}
}