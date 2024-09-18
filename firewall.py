from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, ipv4, tcp, udp, icmp
import logging

class AdvancedFirewall(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(AdvancedFirewall, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.blocked_ips = ['10.0.0.1']  # Example IP to block
        self.blocked_ports = [22, 80]  # Example ports to block (SSH and HTTP)
        self.logger.setLevel(logging.INFO)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # Handle IP packets
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        if ip_pkt:
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst

            # Block traffic from specific IP addresses
            if src_ip in self.blocked_ips or dst_ip in self.blocked_ips:
                self.logger.info(f"Blocked packet from {src_ip} to {dst_ip}")
                return  # Drop the packet

            # Handle TCP/UDP for port blocking
            tcp_pkt = pkt.get_protocol(tcp.tcp)
            udp_pkt = pkt.get_protocol(udp.udp)

            # Block specific TCP or UDP ports
            if tcp_pkt and tcp_pkt.dst_port in self.blocked_ports:
                self.logger.info(f"Blocked TCP packet on port {tcp_pkt.dst_port} from {src_ip} to {dst_ip}")
                return  # Drop the packet
            elif udp_pkt and udp_pkt.dst_port in self.blocked_ports:
                self.logger.info(f"Blocked UDP packet on port {udp_pkt.dst_port} from {src_ip} to {dst_ip}")
                return  # Drop the packet

            # Block ICMP (ping) traffic
            if ip_pkt.proto == 1:  # ICMP
                self.logger.info(f"Blocked ICMP packet from {src_ip} to {dst_ip}")
                return  # Drop the packet

        # Forward other traffic normally
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port, actions=actions)
        datapath.send_msg(out)
