package com.swp.ontop.ui.dashboard

import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.MediaController
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.swp.ontop.R
import com.swp.ontop.databinding.FragmentDashboardBinding

class DashboardFragment : Fragment() {

    private lateinit var dashboardViewModel: DashboardViewModel
    private var _binding: FragmentDashboardBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        dashboardViewModel =
            ViewModelProvider(this).get(DashboardViewModel::class.java)

        _binding = FragmentDashboardBinding.inflate(inflater, container, false)
        val root: View = binding.root

        val camView = binding.camView
        val mediaController = MediaController(activity?.applicationContext)
        mediaController.setAnchorView(camView)
        val uri: Uri = Uri.parse("rtmp://ontop.hs-bochum.de/live")
        camView.setMediaController(mediaController)
        camView.setVideoURI(uri)
        camView.requestFocus()
        camView.start()
        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}