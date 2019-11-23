package network.branch;

import network.core.Packet;
import network.branch.threads.DedicatedLeafServicer;
import network.branch.threads.LeafPruningThread;
import network.core.NodeLocation;

import java.io.IOException;
import java.net.SocketException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import cps.management.LeafManager;
import logging.SmartLog;

/**
 * Branch allows for a logical grouping of one or more
 * leaves to facilitate broadcasting of messages.
 * 
 * @since October 16, 2019
 * @author Ahmed Sakr
 */
public class Branch {

    // The logger instance for this class.
    private static SmartLog logger = new SmartLog(Branch.class.getName());

    // The list of live nodes connected to this stem.
    private ArrayList<DedicatedLeafServicer> servicers;
    private LeafManager manager;
    private String name;
    private LeafPruningThread pruner;

    /**
     * Initializes the branch with a random port.
     */
    public Branch(String name) {
        this.servicers = new ArrayList<>();
        this.name = name;

        this.pruner = new LeafPruningThread(this);
    }
    
    /**
     * Retrieve the currently active leaf servicers.
     * 
     * @return A list of all DedicatedLeafServicers on this branch.
     */
    public synchronized ArrayList<DedicatedLeafServicer> getServicers() {
        return this.servicers;
    }

    /**
     * Retrieve the name of this branch.
     *
     * @return A string name of this branch.
     */
    public String getName() {
        return this.name;
    }

    /**
     * Check if the provided leaf is being serviced by any of the existing servicers.
     * 
     * @param leaf The IPv4 address and port of the leaf
     * @return      true    If the leaf has an existing servicer (i.e., has been registered)
     *              false   Otherwise
     */
    public boolean isExistingLeaf(NodeLocation leaf) {
        return this.getServicer(leaf) != null;
    }

    /**
     * Retrieve the dedicated leaf servicer for the specified leaf.
     * 
     * @param leaf  The IPv4 address and port of the leaf
     * @return      The DedicatedLeafServicer Object of that leaf if it exists.
     *              Otherwise, null.
     */
    public DedicatedLeafServicer getServicer(NodeLocation leaf) {

        // Search the list using the NodeLocation as the search criterion.
        List<DedicatedLeafServicer> query =
            this.servicers.stream()
                .filter((servicer) -> servicer.getDestination().equals(leaf))
                .collect(Collectors.toList());

        // Check if the query yielded a match or if it came back empty.
        if (query.size() == 1) {
            return query.get(0);
        } else {
            return null;
        }
    }

    /**
     * Spawn a new servicer for the leaf specified by the location.
     * 
     * @param location The IPv4 address of the leaf
     */
    public synchronized void addLeaf(NodeLocation location) throws SocketException {
        logger.info("Adding a new leaf servicer for " + location);
        this.servicers.add(new DedicatedLeafServicer(this, location));
    }

    /**
     * Removes an existing servicer for the leaf speicified by the location.
     * 
     * @param location The IPv4 address of the leaf
     */
    public synchronized void removeLeaf(NodeLocation location) {
        for (DedicatedLeafServicer servicer : this.servicers) {
            if (servicer.getDestination().equals(location)) {
                logger.info("Stop leaf servicer for " + location);
                servicer.stop();
                this.servicers.remove(servicer);
                break;
            }
        }
    }

    /**
     * Attach a leaf manager that the dedicated leaf managers on this branch
     * will invoke when handling the interactions with their leaves.
     *
     * @param manager The LeafManager instance that dictates the interactions
     *                with the leaves on this branch.
     */
    public void attachManager(LeafManager manager) {
        this.manager = manager;
    }

    /**
     * Manage a packet received by a DedicatedLeafServicer.
     *
     * @param packet The received packet by the servicer.
     * @return The status of the management operation
     */
    public Packet manage(Packet packet) {
        if (this.manager == null) {
            return null;
        }

        return this.manager.handle(packet);
    }

    /**
     * Send a message to all leaves on this branch.
     * 
     * @param packet The packet to broadcast to all leaves
     */
    public synchronized void broadcast(Packet packet) throws IOException {
        logger.debug("Broadcasting packet to all leaves");

        for (DedicatedLeafServicer servicer : this.servicers) {
            servicer.forwardBroadcast(packet);
        }
    }

    /**
     * Override the default Object toString() method to return the name of this branch.
     * 
     * @return The name of this branch.
     */
    @Override
    public String toString() {
        return this.name;
    }
}